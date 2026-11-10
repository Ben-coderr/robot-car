// ============================================================================
//  TEST 06 - PARKING ALARM ON THE BENCH  (Arduino UNO only)
//
//  The bridge between the "Learn Arduino" website and our robot car:
//    learn-arduino-red.vercel.app  lesson 7  (Read a sensor)  -> HC-SR04 + pulseIn
//                                  lesson 8  (Make a sound)   -> buzzer
//                                  lesson 16 (Parking sensor) -> zones with comparisons
//  ...rewired on the ROBOT CAR pins, so the same wires stay on the car.
//
//  Wiring (UNO only, no motors, no ESP32-CAM):
//    HC-SR04  VCC -> 5V   GND -> GND   TRIG -> D13   ECHO -> D12
//    Red LED  (alarm)   A0 -> 220 ohm -> LED long leg, short leg -> GND
//    White LED (reverse) A2 -> 220 ohm -> LED long leg, short leg -> GND
//    ACTIVE buzzer      + -> A3,  - -> GND
//
//  Serial Monitor 115200: shows distance, zone and a text "radar bar".
//  Move your hand towards the sensor: beeps get faster, then continuous.
// ============================================================================

const int TRIG = 13, ECHO = 12;          // site lesson 7 used D9 / D10
const int RED_LED = A0, REV_LED = A2, BUZZER = A3;

// Thresholds (same defaults as the car's settings page)
const int WARN_CM = 100;   // beeping starts below this
const int STOP_CM = 20;    // continuous tone below this (the car auto-brakes at 15)

long readCm() {
  digitalWrite(TRIG, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);   // 10 us ping (lesson 7)
  digitalWrite(TRIG, LOW);
  long us = pulseIn(ECHO, HIGH, 30000UL);           // timeout 30 ms = ~5 m
  if (us == 0) return 999;                           // no echo = nothing in range
  return us / 58;                                     // 58 us per cm, there and back
}

// Median of 3 readings: ignores one wrong echo (the car firmware does the same)
long readCmFiltered() {
  long a = readCm(); delay(10);
  long b = readCm(); delay(10);
  long c = readCm();
  if (a > b) { long t = a; a = b; b = t; }
  if (b > c) { long t = b; b = c; c = t; }
  if (a > b) { long t = a; a = b; b = t; }
  return b;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG, OUTPUT); pinMode(ECHO, INPUT);
  pinMode(RED_LED, OUTPUT); pinMode(REV_LED, OUTPUT); pinMode(BUZZER, OUTPUT);
  digitalWrite(REV_LED, HIGH);           // pretend the car is reversing
  Serial.println(F("\n=== TEST 06 : parking alarm bench ==="));
  Serial.println(F("Move your hand towards the sensor."));
}

unsigned long lastToggle = 0, lastPrint = 0;
bool beepOn = false;

void loop() {
  long cm = readCmFiltered();

  // ---- zones: one comparison each, exactly one is true (lesson 16 idea) ----
  bool safe   = cm >  WARN_CM;
  bool warn   = cm >  STOP_CM && cm <= WARN_CM;
  bool danger = cm <= STOP_CM;

  if (safe) {                                  // quiet
    beepOn = false;
  } else if (danger) {                         // continuous tone + LED on
    beepOn = true;
  } else {                                     // closer = faster beeping
    unsigned long period = map(cm, STOP_CM, WARN_CM, 120, 900);   // ms
    if (millis() - lastToggle >= period / 2) {
      lastToggle = millis();
      beepOn = !beepOn;
    }
  }
  digitalWrite(BUZZER, beepOn);                // active buzzer: HIGH = sound
  digitalWrite(RED_LED, beepOn);               // LED flashes with the beep

  if (millis() - lastPrint >= 200) {           // print 5 times a second
    lastPrint = millis();
    char num[8];
    if (cm >= 999) strcpy(num, "  ---"); else snprintf(num, sizeof num, "%5ld", cm);
    Serial.print(num);
    Serial.print(F(" cm  "));
    Serial.print(safe ? F("SAFE  ") : warn ? F("WARN  ") : F("STOP! "));
    int bar = constrain(map(min(cm, 200L), 0, 200, 30, 0), 0, 30);   // longer bar = closer
    for (int i = 0; i < bar; i++) Serial.print('#');
    Serial.println();
  }
}
