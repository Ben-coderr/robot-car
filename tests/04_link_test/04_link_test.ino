/*
 * TEST 4 - SERIAL LINK UNO <-> ESP32-CAM
 * 1. Flash the real firmware (esp32cam_robot) on the ESP32-CAM.
 * 2. Flash THIS sketch on the UNO, keep the UNO on USB, Serial Monitor 115200.
 * 3. Connect the phone to WiFi "RobotCar" and open http://192.168.4.1
 * Expected:
 *   - Phone radar shows a fake distance going 20 -> 200 cm  (UNO -> ESP works)
 *   - Serial Monitor prints "M,0,0*4D" lines, and moving the joystick
 *     changes the numbers                                      (ESP -> UNO works)
 */
#include <SoftwareSerial.h>
SoftwareSerial link(3, 2);   // RX=D3 (from ESP IO14), TX=D2 (divider -> ESP IO15)

void setup() {
  Serial.begin(115200);
  link.begin(38400);
  Serial.println("Link test running...");
}
void loop() {
  static uint32_t last = 0;
  static int fake = 20;
  if (millis() - last > 100) {
    last = millis();
    fake += 5; if (fake > 200) fake = 20;
    link.print("D,90,"); link.print(fake); link.println(",1");
  }
  while (link.available()) Serial.write(link.read());
}
