/*
 * TEST 2 - HC-SR04 ULTRASONIC (Arduino UNO)
 * Open Serial Monitor (or Serial Plotter) at 115200.
 * Move your hand behind the car: the number must follow your hand.
 * "no echo" = nothing within 4 m, or TRIG/ECHO swapped, or no 5V.
 */
const uint8_t TRIG = 13, ECHO = 12;

void setup() {
  Serial.begin(115200);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}
void loop() {
  digitalWrite(TRIG, LOW);  delayMicroseconds(3);
  digitalWrite(TRIG, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  unsigned long us = pulseIn(ECHO, HIGH, 25000UL);
  if (us == 0) Serial.println("no echo");
  else { Serial.print(us / 58); Serial.println(" cm"); }
  delay(100);
}
