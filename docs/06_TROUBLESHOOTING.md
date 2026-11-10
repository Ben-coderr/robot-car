# 06 · Hardware Testing, Diagnostics & Troubleshooting

> **Printable Lab Worksheet**: For laboratory classroom records, see [`docs/pdf/05_Testing_and_Troubleshooting.pdf`](pdf/05_Testing_and_Troubleshooting.pdf).

---

## 1. Hardware Diagnostic Workflow

When assembling and testing your vehicle, follow this sequential diagnostic pipeline to isolate issues before performing full teleoperation runs:

```
[ Power Rail Verification ] ──► [ Individual Motor Run ] ──► [ Sonar & Light Checks ]
           │                               │                               │
       (5.0V OK?)                     (Spin OK?)                      (Sonar OK?)
           │                               │                               │
           ▼                               ▼                               ▼
[ ESP32-CAM Standalone ]  ──► [ UART Serial Handshake ] ──► [ Complete Vehicle Drive ]
      (Camera OK?)                    (Link OK?)                     (Fully Verified)
```

---

## 2. Progressive Hardware Test Sketches

The repository provides six standalone Arduino test sketches located in the `tests/` directory. Each sketch isolates and validates a specific hardware subsystem:

| Test Sketch | Path | Subsystem Tested | Success Criteria |
|:---:|:---|:---|:---|
| **01** | `tests/01_motor_test` | L298N & 4× TT Motors | Wheels rotate: Forward (2s) → Reverse (2s) → Pivot Left (2s) → Pivot Right (2s) |
| **02** | `tests/02_ultrasonic_test` | HC-SR04 Sonar | Serial Monitor (115200 baud) prints distance reading matching physical ruler |
| **03** | `tests/03_buzzer_led_test` | Lights & Active Buzzer | Headlights light, hazard blinks 4 times, buzzer beeps accelerate with proximity |
| **04** | `tests/04_link_test` | Arduino ↔ ESP32 UART | Arduino transmits simulated radar sweep; Serial Monitor displays incoming `M,l,r` commands |
| **05** | `tests/05_esp32cam_test` | ESP32-CAM Module | Standalone Wi-Fi Access Point (`CamTest`); streams live video, captures photo, dims flash |
| **06** | `tests/06_parking_alarm_bench` | Reverse Radar Logic | Simulates approaching obstacle on bench: transitions from SAFE → WARN → STOP! |

---

## 3. Systematic Troubleshooting Matrix

### Power Distribution & System Brownouts

| Symptom | Probable Cause | Corrective Action |
|:---|:---|:---|
| **ESP32 reboots when motors start** (`Brownout detector was triggered`) | Inductive current spike causes 5V rail to dip below 4.5V | 1. Ensure the **2200 µF 16V capacitor** is connected across 5V and GND directly beside the ESP32.<br>2. Confirm ESP32 is powered from the **Arduino 5V pin**, never from the L298N 5V regulator.<br>3. Verify 18650 battery cells are fully charged (≥ 7.4V under load).<br>4. Select **Slow Gear (40%)** in the app to reduce inrush current. |
| **No power LEDs light up when switch closed** | Loose wiring, blown cell, or reversed polarity | 1. Measure battery voltage with a multimeter across switch contacts.<br>2. Check that the daisy-chained wire from L298N `+12V` is securely screwed into Arduino `VIN`.<br>3. Inspect the breadboard ground bridge jumper. |
| **Arduino voltage regulator gets warm** | Normal linear dissipation (Vin = 7.4V → Vout = 5.0V) | A moderately warm regulator (40°C–50°C) is completely normal. If it is scorching hot (> 80°C), check for short circuits on the breadboard 5V bus. Never attach high-current servos directly to this 5V rail. |
| **System shuts down completely at high speed** | Counterfeit or degraded 18650 battery cells | Cheap or unbranded cells (e.g. marked "9900 mAh") have high internal resistance. Under a 2A motor surge, cell voltage collapses. Replace with genuine high-drain 18650 cells. |

---

### Motors & Drive Train

| Symptom | Probable Cause | Corrective Action |
|:---|:---|:---|
| **App shows throttle bars, but motors do not spin** | ENA/ENB jumpers installed or missing battery ground | 1. Confirm that **both black ENA and ENB jumpers have been removed** from the L298N.<br>2. Verify common ground wire exists between L298N GND and breadboard negative rail.<br>3. Check if the app displays a "Car Not Responding" badge (indicates serial link disconnection). |
| **Car spins in circles when driving forward** | One motor pair wired in reverse polarity | Swap the two motor wire leads on the L298N `OUT` screw terminals for that side, or toggle `INVERT_LEFT` / `INVERT_RIGHT` to `true` in `uno_controller.ino`. |
| **Two motors on the same side fight each other** | Individual motor wired backwards | Disconnect one motor of the pair and swap its physical leads to match the rotational direction of its partner. |
| **Motors hum at low throttle without turning** | Static mechanical friction exceeds starting torque | Increase `#define MIN_PWM` in `firmware/uno_controller/uno_controller.ino` from `90` to `115`–`130`. |
| **Car refuses to reverse even in open space** | Rear ultrasonic sensor detects floor reflection | The HC-SR04 sonar is detecting carpet or floor tiles. Increase the mounting height to 10–12 cm or tilt the sensor upward by 3°–5°. |

---

### Camera & Wireless Connectivity

| Symptom | Probable Cause | Corrective Action |
|:---|:---|:---|
| **Serial Monitor logs `Camera init FAILED`** | Ribbon cable loose or incorrect board selection | 1. Open the black FPC latch, re-seat the golden contacts of the camera ribbon cable, and snap the latch shut.<br>2. Confirm board is selected as **AI Thinker ESP32-CAM** with **Huge APP** partition scheme. |
| **Wi-Fi SSID `RobotCar` does not appear** | ESP32-CAM in bootloader mode or unpowered | 1. Ensure pin **IO0 is NOT connected to GND** during normal operation.<br>2. Tap the **RST** button on the ESP32 board.<br>3. Verify that `STA_SSID` is empty in `config.h` (otherwise it attempts to connect to an external router). |
| **Smartphone drops Wi-Fi connection** | Phone OS automatically switches to mobile data | In phone Wi-Fi settings, tap `RobotCar` and select **"Stay connected"** or temporarily disable mobile cellular data while operating the car. |
| **Video stream lags or stutters** | RF interference or high resolution | 1. Switch resolution to **QVGA (320×240)** and JPEG quality to **15–20** in app settings.<br>2. Ensure ESP32 on-board PCB antenna is positioned away from the motor driver heatsink. |

---

### Sensors, Audio & Lighting

| Symptom | Probable Cause | Corrective Action |
|:---|:---|:---|
| **App display shows "Waiting for Sensor..."** | UART serial link disconnected between boards | 1. Verify Arduino `D2` connects to the 1k/2k voltage divider and into ESP32 `IO15`.<br>2. Verify ESP32 `IO14` connects directly to Arduino `D3`.<br>3. Ensure both microcontrollers share a common ground reference. |
| **Ultrasonic distance permanently reads 0 or > 400** | TRIG and ECHO signal wires reversed | Swap Arduino pins `D12` and `D13` or check for loose jumper connections at the sensor socket. |
| **Buzzer stays silent but red alarm LED flashes** | Passive buzzer used instead of active buzzer | Replace buzzer with a **5V Active Buzzer** (has a removable protective sticker and sounds continuously when connected across 5V and GND). Check if "Mute" is toggled on in app settings. |
| **Headlights do not illuminate** | Incorrect pin row or reversed LED polarity | 1. Verify headlights connect to breadboard row 24 (Arduino `A4`).<br>2. Check that the long lead (Anode, +) faces row 24 and the short lead (Cathode, −) connects to ground.<br>3. Ensure the top breadboard ground rail is bridged to the bottom ground rail. |

---

## 4. Multimeter Test Point Verification Guide

Before powering on for the first time, take measurements with a digital voltmeter across the following test points with the battery switch turned ON:

| Test Measurement | Multimeter Positive Probe (+) | Multimeter Negative Probe (−) | Expected Voltage Reading | Diagnostic Interpretation |
|:---|:---|:---|:---:|:---|
| **Battery Terminal** | Switch Output Terminal | Battery Pack Ground Lead | **7.2V – 8.4V** | If < 6.8V, recharge the 18650 cells immediately |
| **Logic Bus Rail** | Breadboard 5V Positive Rail | Breadboard Ground Rail | **4.90V – 5.15V** | Regulated logic output from Arduino Uno onboard LDO |
| **ESP32 Supply** | ESP32-CAM 5V Pin | ESP32-CAM GND Pin | **4.85V – 5.10V** | While driving motors, must never drop below 4.75V |
| **UART RX Level** | ESP32-CAM Pin IO15 | Breadboard Ground Rail | **3.1V – 3.35V** | **Must NEVER exceed 3.6V!** (Verifies 1k/2k divider) |
| **UART TX Level** | Arduino Pin D3 (RX) | Breadboard Ground Rail | **3.0V – 3.3V** | Confirms valid logic HIGH transmitted by ESP32 IO14 |
