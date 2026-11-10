/*
 * TEST 3 - LIGHTS + BUZZER (Arduino UNO)
 *
 * Wiring (same as the car):
 *   A0 -> 220 ohm -> RED rear LED     -> GND
 *   A2 -> 220 ohm -> WHITE reverse LED -> GND
 *   A3 -> ACTIVE buzzer (+)            , buzzer (-) -> GND
 *   A4 -> 220 ohm -> WHITE headlight 1 -> GND
 *   A4 -> 220 ohm -> WHITE headlight 2 -> GND   (each LED has its OWN resistor)
 *
 * What you should see / hear (Serial Monitor 115200 shows each step):
 *   1. Headlights ON for 2 s, then 4 hazard blinks (headlights + red LED together)
 *   2. Parking-sensor simulation: white reverse LED on, slow beeps -> faster ->
 *      continuous, with the red LED flashing in sync.
 *
 * Silent but the LEDs work? You probably have a PASSIVE buzzer: buy an ACTIVE 5 V one
 * (an active buzzer beeps when you connect it straight to 5 V).
 * Only one headlight lights? Check that LED's legs (long leg = + towards the resistor).
 */
const uint8_t BUZZER = A3, LED = A0, REVLED = A2, HEAD = A4;

void beep(bool on) {
  digitalWrite(BUZZER, on);
  digitalWrite(LED, on);
}

void setup() {
  Serial.begin(115200);
  pinMode(BUZZER, OUTPUT); pinMode(LED, OUTPUT); pinMode(REVLED, OUTPUT); pinMode(HEAD, OUTPUT);
}

void loop() {
  Serial.println("1) Headlights ON");
  digitalWrite(HEAD, HIGH); delay(2000);
  Serial.println("   Hazard: headlights + red LED blink");
  for (int i = 0; i < 4; i++) {
    digitalWrite(HEAD, HIGH); digitalWrite(LED, HIGH); delay(500);
    digitalWrite(HEAD, LOW);  digitalWrite(LED, LOW);  delay(500);
  }

  Serial.println("2) Reversing - parking sensor simulation");
  digitalWrite(REVLED, HIGH);
  for (int period = 900; period >= 120; period -= 130) {   // object getting closer
    Serial.print("   beep period "); Serial.println(period);
    for (int i = 0; i < 3; i++) { beep(true); delay(period / 2); beep(false); delay(period / 2); }
  }
  Serial.println("   DANGER - continuous");
  beep(true); delay(1500); beep(false);
  digitalWrite(REVLED, LOW);
  delay(2000);
}
