#pragma once
// ============================================================================
//  ROBOT CAR - ESP32-CAM configuration. Edit this file, not the .ino
// ============================================================================

// ---------------------------------------------------------------- WiFi ------
// Mode 1 (default): the car creates its own WiFi network. Phone connects to it
// and opens http://192.168.4.1
#define AP_SSID      "RobotCar"
#define AP_PASSWORD  "12345678"      // at least 8 characters
#define AP_CHANNEL   6

// Mode 2 (optional): join your home WiFi / phone hotspot instead.
// Leave STA_SSID empty "" to always use Mode 1.
// If joining fails within 10 s the car falls back to Mode 1.
#define STA_SSID     ""
#define STA_PASSWORD ""

// ---------------------------------------------------------- Serial link -----
// UART to the Arduino UNO (do NOT use GPIO1/3: they are for programming)
#define LINK_RX_PIN  15   // <- from UNO D2 through 1k/2k voltage divider
#define LINK_TX_PIN  14   // -> to UNO D3
#define LINK_BAUD    38400

// ---------------------------------------------------------------- LEDs ------
#define FLASH_LED_PIN   4    // big white LED on the ESP32-CAM ("Cam light" in the app)
#define STATUS_LED_PIN  33   // small red LED on the back of the board (active LOW)

// --------------------------------------------------------------- Safety -----
#define PHONE_TIMEOUT_MS  500   // no drive command from phone -> stop the car
#define HEARTBEAT_MS      150   // how often the last command is re-sent to the UNO

// ---------------------------------------------------------------- Camera ----
// FRAMESIZE_QVGA (320x240) provides high frame rate (25-30 FPS) on all sensors
#define CAM_FRAMESIZE   FRAMESIZE_QVGA
#define CAM_QUALITY     12      // 10 (best) .. 63 (worst). 10-15 is good for OV2640.
#define CAM_VFLIP       0       // set 1 if the image is upside down
#define CAM_HMIRROR     0

// Only if the board keeps rebooting with "Brownout detector was triggered"
// AND you cannot fix the power supply yet. Fixing the power is the real cure.
#define DISABLE_BROWNOUT 1
