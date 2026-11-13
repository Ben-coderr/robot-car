/*
 * ============================================================================
 *  ROBOT CAR - Arduino UNO / NANO "body controller"
 * ============================================================================
 *  Job of this board:
 *    - Drive the 4 DC motors through the L298N (speed + direction)
 *    - Measure the distance BEHIND the car with the HC-SR04
 *    - Rear parking alarm: buzzer + flashing LED while reversing
 *    - Front headlights (2 white LEDs): off / on / hazard blink, from the app
 *    - Auto-brake: refuse to reverse into an obstacle (configurable)
 *    - Safety: stop the motors if the ESP32-CAM / phone goes silent
 *    - Optional: sweep the HC-SR04 with an SG90 servo for a real radar scan
 *
 *  It talks to the ESP32-CAM (camera + WiFi + web app) over a serial link:
 *      ESP32-CAM  --->  UNO   : commands     (M, H, C, L ...)
 *      UNO        --->  ESP32 : sensor data  (D ...)
 *  The full protocol is documented in docs/05_PROTOCOL.md
 *
 *  Board : Arduino Uno (or Nano, same pins)       Core : Arduino AVR Boards
 *  Libs  : none (SoftwareSerial + Servo are built in)
 * ============================================================================
 */

#include <Arduino.h>
#include <SoftwareSerial.h>

// ---------------------------------------------------------------- OPTIONS ---
#define USE_SERVO        0     // 1 = HC-SR04 mounted on SG90 servo (radar sweep)
#define DEBUG_USB        1     // 1 = print debug text on the USB serial monitor

#if USE_SERVO
  #include <Servo.h>
#endif

// ------------------------------------------------------------------- PINS ---
// L298N motor driver  (remove the ENA / ENB jumpers on the L298N!)
// Chosen so the 6 wires run side by side: L298N ENA IN1 IN2 IN3 IN4 ENB
//                                      -> UNO   D11 D10  D9  D8  D7  D6
const uint8_t PIN_ENA = 11;   // PWM  -> L298N ENA  (LEFT  side speed)
const uint8_t PIN_IN1 = 10;   //      -> L298N IN1
const uint8_t PIN_IN2 = 9;    //      -> L298N IN2
const uint8_t PIN_IN3 = 8;    //      -> L298N IN3
const uint8_t PIN_IN4 = 7;    //      -> L298N IN4
const uint8_t PIN_ENB = 6;    // PWM  -> L298N ENB  (RIGHT side speed)

// HC-SR04 ultrasonic (rear)
const uint8_t PIN_TRIG = 13;
const uint8_t PIN_ECHO = 12;

// Rear warning
const uint8_t PIN_BUZZER = A3;  // ACTIVE 5 V buzzer +
const uint8_t PIN_LED    = A0;  // red rear LED(s) through 220-330 ohm resistor
const uint8_t PIN_REVLED = A2;  // OPTIONAL white "reverse light" LED (220-330 ohm)

// Front headlights: 2 white LEDs, EACH with its own 220 ohm resistor, both on A4
const uint8_t PIN_HEADLIGHT = A4;

// Optional servo
const uint8_t PIN_SERVO = A1;

// Serial link to ESP32-CAM
const uint8_t PIN_LINK_RX = 3;  // <- ESP32-CAM IO14 (TX)  (direct wire, 3.3V is read fine)
const uint8_t PIN_LINK_TX = 2;  // -> 1k/2k divider -> ESP32-CAM IO15 (RX)
const long    LINK_BAUD   = 38400;

// ------------------------------------------------------------ TUNING -------
// Flip these if one side of the car turns the wrong way (instead of swapping wires)
const bool INVERT_LEFT  = false;
const bool INVERT_RIGHT = false;
// Set true if your car's wiring/app causes backward motion to use positive values:
const bool INVERT_REVERSE_DIR = false;
bool invertReverseWarning = INVERT_REVERSE_DIR;

const uint8_t  MIN_PWM          = 90;    // below this the motors only hum: map 1..255 -> MIN_PWM..255
const uint8_t  RAMP_STEP        = 18;    // max PWM change per 10 ms (soft start, protects ESP32 power)
const uint16_t CMD_TIMEOUT_MS   = 1000;  // no command for this long -> stop (1s tolerance for WiFi jitter)
const uint16_t MEASURE_EVERY_MS = 60;    // HC-SR04 needs >= 60 ms between pings
const uint16_t MAX_DIST_CM      = 400;   // HC-SR04 maximum range
const int16_t  REVERSE_THRESHOLD = -20;  // (left+right)/2 below this = "reversing"

// Runtime settings (the phone can change them with the C command)
uint16_t warnDist   = 100;   // cm : start beeping below this
uint16_t stopDist   = 15;    // cm : auto-brake + continuous tone below this
bool     autoBrake  = true;  // block reversing when closer than stopDist
bool     alarmAlways = false;// beep even when not reversing
bool     muted      = false; // silence buzzer (LED still flashes)

// ----------------------------------------------------------------- STATE ---
SoftwareSerial link(PIN_LINK_RX, PIN_LINK_TX);
#if USE_SERVO
Servo radarServo;
int  servoAngle = 90;
int  servoDir   = 1;
const int SERVO_MIN = 30, SERVO_MAX = 150, SERVO_STEP = 10;
#endif

int16_t  targetL = 0, targetR = 0;   // requested speed  -255..255
int16_t  outL = 0, outR = 0;         // ramped speed actually applied
uint32_t lastCmdMs  = 0;
uint32_t lastRampMs = 0;
uint32_t lastMeasMs = 0;
bool     hornOn = false;
uint8_t  lightMode = 0;              // headlights: 0 off, 1 on, 2 hazard (blink)
bool     headOut = false;            // headlights are lit right now

uint16_t distCm = 0;            // 0 = nothing in range
uint16_t hist[3] = {0, 0, 0};   // median filter
uint8_t  histIdx = 0;

bool reversing = false, alarmActive = false, blocked = false;

char     rxBuf[48];
uint8_t  rxLen = 0;

// ============================================================== MOTORS =====
void setSide(int16_t v, uint8_t pinEn, uint8_t pinA, uint8_t pinB, bool invert) {
  if (invert) v = -v;
  if (v == 0) {                       // coast
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
    analogWrite(pinEn, 0);
    return;
  }
  uint8_t pwm = map(abs(v), 1, 255, MIN_PWM, 255);
  digitalWrite(pinA, v > 0 ? HIGH : LOW);
  digitalWrite(pinB, v > 0 ? LOW  : HIGH);
  analogWrite(pinEn, pwm);
}

int16_t rampTo(int16_t cur, int16_t target) {
  // Changing direction: go through zero first
  if ((cur > 0 && target < 0) || (cur < 0 && target > 0)) target = 0;
  if (target > cur) { int16_t n = cur + RAMP_STEP; return n > target ? target : n; }
  if (target < cur) { int16_t n = cur - RAMP_STEP; return n < target ? target : n; }
  return cur;
}

void updateMotors() {
  int16_t l = targetL, r = targetR;

  // If invertReverseWarning is true, positive PWM moves the car backward in the room!
  reversing = invertReverseWarning ? (((l + r) / 2) > -REVERSE_THRESHOLD) : (((l + r) / 2) < REVERSE_THRESHOLD);
  blocked   = autoBrake && reversing && distCm > 0 && distCm <= stopDist;
  if (blocked) {                      // cancel only the backward part
    if (invertReverseWarning) {
      if (l > 0) l = 0;
      if (r > 0) r = 0;
    } else {
      if (l < 0) l = 0;
      if (r < 0) r = 0;
    }
  }

  if (millis() - lastRampMs >= 10) {
    lastRampMs = millis();
    // Instant stop when braking, soft ramp otherwise
    outL = (l == 0 && blocked) ? 0 : rampTo(outL, l);
    outR = (r == 0 && blocked) ? 0 : rampTo(outR, r);
    setSide(outL, PIN_ENA, PIN_IN1, PIN_IN2, INVERT_LEFT);
    setSide(outR, PIN_ENB, PIN_IN3, PIN_IN4, INVERT_RIGHT);
  }
}

// ========================================================== ULTRASONIC =====
uint16_t pingCm() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(3);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  // 25 ms timeout ~ 4.3 m. Returns 0 if no echo.
  unsigned long us = pulseIn(PIN_ECHO, HIGH, 25000UL);
  if (us == 0) return 0;
  uint16_t cm = us / 58;
  if (cm < 2 || cm > MAX_DIST_CM) return 0;
  return cm;
}

uint16_t median3(uint16_t a, uint16_t b, uint16_t c) {
  if (a > b) { uint16_t t = a; a = b; b = t; }
  if (b > c) { uint16_t t = b; b = c; c = t; }
  if (a > b) { uint16_t t = a; a = b; b = t; }
  return b;
}

void measure() {
  uint16_t cm = pingCm();
#if USE_SERVO
  // While sweeping each angle is a new target: no filtering across angles
  distCm = cm;
  int angleNow = servoAngle;
  servoAngle += servoDir * SERVO_STEP;
  if (servoAngle >= SERVO_MAX || servoAngle <= SERVO_MIN) servoDir = -servoDir;
  radarServo.write(servoAngle);       // move now, it settles before next ping
#else
  // "0" (nothing in range) counts as far away for the filter
  hist[histIdx] = cm == 0 ? 999 : cm;
  histIdx = (histIdx + 1) % 3;
  uint16_t m = median3(hist[0], hist[1], hist[2]);
  distCm = (m >= 999) ? 0 : m;
  int angleNow = 90;
#endif

  // Report to ESP32:  D,<angle>,<cm>,<flags>
  uint8_t flags = (reversing ? 1 : 0) | (alarmActive ? 2 : 0) | (blocked ? 4 : 0) | (hornOn ? 8 : 0)
                | (headOut ? 16 : 0) | (lightMode == 2 ? 32 : 0);
  link.print(F("D,"));
  link.print(angleNow);
  link.print(',');
  link.print(distCm);
  link.print(',');
  link.println(flags);

#if DEBUG_USB
  Serial.print(F("dist=")); Serial.print(distCm);
  Serial.print(F(" L=")); Serial.print(outL);
  Serial.print(F(" R=")); Serial.print(outR);
  Serial.print(F(" flags=")); Serial.println(flags);
#endif
}

// ======================================================= BUZZER + LED =====
#if !USE_SERVO
// Hardware-timed square wave tone generator using Timer1 CTC.
// Works for BOTH Passive and Active buzzers on pin A3 (PC3) without conflicting with Timer2 PWM on D11/ENA!
static volatile bool buzzerRunning = false;

void buzzerInit() {
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
}

void buzzer(bool on, uint16_t freqHz = 2500) {
  if (!on || freqHz == 0) {
    if (buzzerRunning) {
      TIMSK1 &= ~(1 << OCIE1A);                            // Silence tone without tearing down CTC timer
      digitalWrite(PIN_BUZZER, LOW);
    }
    return;
  }

  // Calculate OCR1A for desired frequency:
  // freqHz is the audio tone frequency (e.g. 2000 Hz horn or 2400 Hz parking beep)
  // OCR1A = (16,000,000 / (8 * (freqHz * 2))) - 1 = (1,000,000 / freqHz) - 1
  uint16_t ocr = (1000000UL / freqHz) - 1;
  OCR1A = ocr;

  if (!buzzerRunning) {
    TCNT1  = 0;
    TCCR1A = 0;
    TCCR1B = (1 << WGM12) | (1 << CS11);                  // CTC mode, prescaler 8
    buzzerRunning = true;
  }
  TIMSK1 |= (1 << OCIE1A);                                // Enable compare match interrupt
}

void buzzerStop() {
  if (buzzerRunning) {
    TIMSK1 &= ~(1 << OCIE1A);                              // Disable interrupt
    TCCR1A = (1 << WGM10);                                // Restore Arduino default PWM mode
    TCCR1B = (1 << CS11) | (1 << CS10);                   // Restore Arduino default prescaler 64
    digitalWrite(PIN_BUZZER, LOW);
    buzzerRunning = false;
  }
}

// Ultra-fast naked ISR: exactly 2 CPU instructions (sbi + reti = 6 cycles = 375 ns!)
// Zero register pushes, zero SREG side effects, cannot disrupt SoftwareSerial or PWM
ISR(TIMER1_COMPA_vect, ISR_NAKED) {
  asm volatile(
    "sbi %0, %1 \n\t"
    "reti \n\t"
    :: "I" (_SFR_IO_ADDR(PINC)), "I" (3)
  );
}

#else
// Fallback if Servo is active on Timer1
void buzzerInit() {
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
}
void buzzer(bool on, uint16_t freqHz = 2500) {
  digitalWrite(PIN_BUZZER, on ? HIGH : LOW);
}
void buzzerStop() {
  digitalWrite(PIN_BUZZER, LOW);
}
#endif

// ====================================================== RETRO MELODY =======
struct MelodyNote {
  uint16_t freq;     // Frequency in Hz (0 = rest)
  uint16_t dur;      // Duration in ms
};

// Super Mario Bros - Iconic 8-bit Main Theme (high octave, sweet buzzer frequencies)
const MelodyNote MARIO_THEME[] PROGMEM = {
  // Opening fanfare (E6, C6, G6, G5)
  {1319, 120}, {0, 40}, {1319, 120}, {0, 160}, {1319, 120}, {0, 160},
  {1047, 120}, {0, 40}, {1319, 160}, {0, 140}, {1568, 240}, {0, 200},
  {784, 240},  {0, 240},

  // Main theme phrase
  {1047, 180}, {0, 80}, {784, 180},  {0, 80}, {659, 180},  {0, 80},
  {880, 160},  {0, 40}, {988, 160},  {0, 40}, {932, 140},  {0, 40},
  {880, 160},  {0, 40}, {784, 140},  {1319, 140}, {1568, 140},
  {1760, 200}, {0, 50}, {1397, 140}, {1568, 140}, {0, 50},
  {1319, 160}, {0, 40}, {1047, 140}, {1175, 140}, {988, 240}, {0, 80}
};
const uint8_t MARIO_NOTES_COUNT = sizeof(MARIO_THEME) / sizeof(MARIO_THEME[0]);

static bool     songActive = false;
static uint8_t  songStep   = 0;
static uint32_t songNextMs = 0;

void songStart() {
  songActive = true;
  songStep   = 0;
  songNextMs = millis();
}

void songStop() {
  if (songActive) {
    songActive = false;
    songStep   = 0;
    buzzerStop();
    bool hazardBlink = lightMode == 2 && (millis() % 1000) < 500;
    digitalWrite(PIN_HEADLIGHT, (lightMode == 1 || hazardBlink) ? HIGH : LOW);
  }
}

void updateSong() {
  if (!songActive) return;

  // Let reverse alarm or manual horn instantly override
  if (hornOn || alarmActive) {
    songStop();
    return;
  }

  uint32_t now = millis();
  if (now >= songNextMs) {
    if (songStep >= MARIO_NOTES_COUNT) {
      songStop();
      return;
    }

    uint16_t f = pgm_read_word(&MARIO_THEME[songStep].freq);
    uint16_t d = pgm_read_word(&MARIO_THEME[songStep].dur);
    songStep++;

    if (f > 0 && !muted) {
      buzzer(true, f);
      digitalWrite(PIN_HEADLIGHT, HIGH);
    } else {
      buzzer(false);
      if (lightMode != 1) digitalWrite(PIN_HEADLIGHT, LOW);
    }
    songNextMs = now + d;
  }
}

void updateAlarm() {
  alarmActive = (reversing || blocked || alarmAlways) && distCm > 0 && distCm < warnDist;

  digitalWrite(PIN_REVLED, reversing ? HIGH : LOW);

  if (songActive) {
    if (alarmActive || hornOn) {
      songStop();
    } else {
      // Song is actively driving the buzzer; do not overwrite
      return;
    }
  }

  bool on;
  uint16_t toneFreq = 2500;
  if (hornOn) {
    on = true;
    toneFreq = 2000; // Powerful automotive horn tone!
  } else if (!alarmActive) {
    on = false;
  } else if (distCm <= stopDist + 5) {
    on = true;                                   // DANGER: continuous loud tone!
    toneFreq = 2800; // Urgent high-frequency warning tone!
  } else {
    // Parking-sensor style: the closer, the faster it beeps
    uint16_t period = map(constrain(distCm, stopDist + 5, warnDist),
                          stopDist + 5, warnDist, 100, 700);
    on = (millis() % period) < (period / 2);
    toneFreq = 2400; // Crisp sonar ping beep!
  }

  // Hazard mode: headlights and the rear red LED blink together (1 Hz)
  bool hazardBlink = lightMode == 2 && (millis() % 1000) < 500;
  digitalWrite(PIN_LED, (on || blocked || (hazardBlink && !alarmActive)) ? HIGH : LOW);
  buzzer(on && !muted, toneFreq);

  headOut = lightMode == 1 || hazardBlink;
  digitalWrite(PIN_HEADLIGHT, headOut ? HIGH : LOW);
}

// ========================================================= COMMANDS =======
// M,<left>,<right>          motor speeds -255..255
// H,<0|1>                   horn
// C,<warn>,<stop>,<autoBrake>,<always>,<mute>   settings
// L,<0|1|2>                 headlights off / on / hazard blink
// S                         emergency stop
void handleLine(char *line) {
  char *tok = strtok(line, ",");
  if (!tok) return;
  char c = tok[0];

  if (c == 'M') {
    char *a = strtok(NULL, ",");
    char *b = strtok(NULL, ",");
    if (!a || !b) return;
    targetL = constrain(atoi(a), -255, 255);
    targetR = constrain(atoi(b), -255, 255);
    lastCmdMs = millis();
  } else if (c == 'S') {
    targetL = targetR = 0;
    songStop();
    lastCmdMs = millis();
  } else if (c == 'H') {
    char *a = strtok(NULL, ",");
    hornOn = a && atoi(a) == 1;
    if (hornOn) songStop();
  } else if (c == 'P') {
    char *a = strtok(NULL, ",");
    if (a && atoi(a) == 1) songStart();
    else songStop();
  } else if (c == 'L') {
    char *a = strtok(NULL, ",");
    if (a) lightMode = constrain(atoi(a), 0, 2);
  } else if (c == 'C') {
    char *p[5];
    for (uint8_t i = 0; i < 5; i++) { p[i] = strtok(NULL, ","); if (!p[i]) return; }
    warnDist    = constrain(atoi(p[0]), 20, 300);
    stopDist    = constrain(atoi(p[1]), 5, 100);
    if (stopDist + 10 > warnDist) warnDist = stopDist + 10;
    autoBrake   = atoi(p[2]) == 1;
    alarmAlways = atoi(p[3]) == 1;
    muted       = atoi(p[4]) == 1;
    char *p5 = strtok(NULL, ",");
    if (p5) invertReverseWarning = (atoi(p5) == 1);
  }
}

// Lines from the ESP end with "*XX" = XOR of all characters before '*', in hex.
// SoftwareSerial can lose bytes while we transmit, so a damaged line is dropped
// (the ESP re-sends the drive command every 150 ms anyway).
// The "*XX" is removed from the line when it is valid.
bool checksumOk(char *line) {
  char *star = strrchr(line, '*');
  if (!star) return true; // Accept direct/unchecksummed commands for testing
  if (strlen(star) != 3) return false;
  uint8_t cs = 0;
  for (char *c = line; c < star; c++) cs ^= (uint8_t)*c;
  uint8_t got = (uint8_t)strtoul(star + 1, NULL, 16);
  *star = 0;
  return cs == got;
}

void readLink() {
  while (link.available()) {
    char ch = link.read();
    if (ch == '\r') continue;
    if (ch == '\n') {
      rxBuf[rxLen] = 0;
      if (rxLen && checksumOk(rxBuf)) {
#if DEBUG_USB
        // Log received command
        if (rxBuf[0] == 'M') {
          static uint32_t lastPrintCmd = 0;
          if (millis() - lastPrintCmd > 250) {
            lastPrintCmd = millis();
            Serial.print(F("CMD: ")); Serial.println(rxBuf);
          }
        }
#endif
        handleLine(rxBuf);
      }
      rxLen = 0;
    } else if (rxLen < sizeof(rxBuf) - 1) {
      rxBuf[rxLen++] = ch;
    } else {
      rxLen = 0;                       // garbage / overflow: drop line
    }
  }
}

// ============================================================ SETUP =======
void setup() {
  pinMode(PIN_ENA, OUTPUT); pinMode(PIN_ENB, OUTPUT);
  pinMode(PIN_IN1, OUTPUT); pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_IN3, OUTPUT); pinMode(PIN_IN4, OUTPUT);
  setSide(0, PIN_ENA, PIN_IN1, PIN_IN2, false);
  setSide(0, PIN_ENB, PIN_IN3, PIN_IN4, false);

  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  buzzerInit();
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_REVLED, OUTPUT);
  pinMode(PIN_HEADLIGHT, OUTPUT);

#if USE_SERVO
  radarServo.attach(PIN_SERVO);
  radarServo.write(servoAngle);
#endif

#if DEBUG_USB
  Serial.begin(115200);
  Serial.println(F("Robot car UNO controller ready"));
#endif
  link.begin(LINK_BAUD);

  // Boot self-test: short beep + LED flash so you know the board is alive
  digitalWrite(PIN_LED, HIGH); digitalWrite(PIN_HEADLIGHT, HIGH); buzzer(true); delay(120);
  digitalWrite(PIN_LED, LOW);  digitalWrite(PIN_HEADLIGHT, LOW);  buzzer(false);
}

// ============================================================= LOOP =======
void loop() {
  readLink();

  // Fail-safe: lost contact with the ESP32 / phone -> stop
  if (millis() - lastCmdMs > CMD_TIMEOUT_MS) {
    targetL = targetR = 0;
    hornOn = false;
    songStop();
  }

  if (millis() - lastMeasMs >= MEASURE_EVERY_MS) {
    lastMeasMs = millis();
    measure();
  }

  updateSong();
  updateMotors();
  updateAlarm();
}
