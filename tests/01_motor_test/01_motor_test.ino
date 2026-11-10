/*
 * TEST 1 - MOTORS (Arduino UNO + L298N)
 * Put the car on a box so the wheels are in the air!
 * Open Serial Monitor at 115200. Sequence repeats:
 *   FORWARD -> BACKWARD -> SPIN LEFT -> SPIN RIGHT -> STOP
 * If a side turns the wrong way: swap that side's two motor wires on the L298N
 * (or set INVERT_LEFT / INVERT_RIGHT in uno_controller.ino).
 */
const uint8_t ENA = 11, IN1 = 10, IN2 = 9, IN3 = 8, IN4 = 7, ENB = 6;
const uint8_t SPEED = 180;   // 0..255

void side(uint8_t en, uint8_t a, uint8_t b, int v) {
  digitalWrite(a, v > 0); digitalWrite(b, v < 0); analogWrite(en, abs(v));
}
void drive(int l, int r, const char *name, uint16_t ms) {
  Serial.println(name);
  side(ENA, IN1, IN2, l); side(ENB, IN3, IN4, r);
  delay(ms);
}
void setup() {
  Serial.begin(115200);
  const uint8_t pins[] = {ENA, IN1, IN2, IN3, IN4, ENB};
  for (uint8_t p : pins) pinMode(p, OUTPUT);
  Serial.println("Motor test - wheels must be off the ground");
  delay(2000);
}
void loop() {
  drive( SPEED,  SPEED, "FORWARD   (all wheels forward)", 2000);
  drive(0, 0, "stop", 700);
  drive(-SPEED, -SPEED, "BACKWARD  (all wheels backward)", 2000);
  drive(0, 0, "stop", 700);
  drive(-SPEED,  SPEED, "SPIN LEFT (left back, right forward)", 1500);
  drive(0, 0, "stop", 700);
  drive( SPEED, -SPEED, "SPIN RIGHT(left forward, right back)", 1500);
  drive(0, 0, "STOP - waiting 3 s", 3000);
}
