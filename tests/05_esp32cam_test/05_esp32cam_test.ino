// ============================================================================
//  TEST 05 - ESP32-CAM ONLY (no UNO, no motors needed)
//
//  Checks: board boots, PSRAM, camera, WiFi access point, live video,
//          photo capture and the white flash LED (GPIO4).
//
//  Board : "AI Thinker ESP32-CAM"      Partition: "Huge APP (3MB No OTA)"
//  Upload, open Serial Monitor at 115200, press RST.
//  Phone/PC: join WiFi "CamTest" / password 12345678, open http://192.168.4.1
//           (or set WIFI_SSID below to use your home WiFi)
//  No extra libraries needed (ESP32 core 2.x or 3.x).
// ============================================================================
#include "esp_camera.h"
#include <WiFi.h>
#include "esp_http_server.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "camera_pins.h"

// Option A (default): the camera makes its own WiFi "CamTest".
const char* AP_SSID = "CamTest";
const char* AP_PASS = "12345678";   // at least 8 characters

// Option B: join your home WiFi / phone hotspot, then open the IP printed in
// the Serial Monitor from any PC or phone on the same network.
// Leave WIFI_SSID empty "" to use Option A. Falls back to A if joining fails.
const char* WIFI_SSID = "";
const char* WIFI_PASS = "";

#define FLASH_LED 4    // big white LED
#define RED_LED   33   // small red LED on the back (active LOW)

httpd_handle_t webServer = NULL, streamServer = NULL;

// ---------------------------------------------------------------- flash -----
void flashSet(uint8_t v) {
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcWrite(FLASH_LED, v);
#else
  ledcWrite(7, v);
#endif
}
void flashInit() {
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcAttachChannel(FLASH_LED, 5000, 8, 7);   // channel 7: camera uses channel 0
#else
  ledcSetup(7, 5000, 8);
  ledcAttachPin(FLASH_LED, 7);
#endif
  flashSet(0);
}

// --------------------------------------------------------------- camera -----
bool cameraInit() {
  camera_config_t c = {};
  c.ledc_channel = LEDC_CHANNEL_0;  c.ledc_timer = LEDC_TIMER_0;
  c.pin_d0 = Y2_GPIO_NUM; c.pin_d1 = Y3_GPIO_NUM; c.pin_d2 = Y4_GPIO_NUM; c.pin_d3 = Y5_GPIO_NUM;
  c.pin_d4 = Y6_GPIO_NUM; c.pin_d5 = Y7_GPIO_NUM; c.pin_d6 = Y8_GPIO_NUM; c.pin_d7 = Y9_GPIO_NUM;
  c.pin_xclk = XCLK_GPIO_NUM; c.pin_pclk = PCLK_GPIO_NUM;
  c.pin_vsync = VSYNC_GPIO_NUM; c.pin_href = HREF_GPIO_NUM;
  c.pin_sccb_sda = SIOD_GPIO_NUM; c.pin_sccb_scl = SIOC_GPIO_NUM;
  c.pin_pwdn = PWDN_GPIO_NUM; c.pin_reset = RESET_GPIO_NUM;
  c.xclk_freq_hz = 20000000;
  c.pixel_format = PIXFORMAT_JPEG;
  if (psramFound()) {
    c.frame_size = FRAMESIZE_VGA; c.jpeg_quality = 12; c.fb_count = 2;
    c.fb_location = CAMERA_FB_IN_PSRAM; c.grab_mode = CAMERA_GRAB_LATEST;
  } else {
    c.frame_size = FRAMESIZE_QVGA; c.jpeg_quality = 15; c.fb_count = 1;
    c.fb_location = CAMERA_FB_IN_DRAM; c.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  }
  esp_err_t err = esp_camera_init(&c);
  if (err != ESP_OK) {
    Serial.printf("  [FAIL] Camera init error 0x%x\n", err);
    Serial.println("         -> ribbon cable not fully in / latch open, or wrong board selected");
    return false;
  }
  sensor_t* s = esp_camera_sensor_get();
  Serial.printf("  [ OK ] Camera found, sensor PID 0x%02X %s\n", s->id.PID,
                s->id.PID == 0x26 ? "(OV2640)" : "");
  return true;
}

// ----------------------------------------------------------------- pages ----
static const char PAGE[] = R"HTML(<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>ESP32-CAM test</title>
<style>body{margin:0;font-family:sans-serif;background:#0b1f3a;color:#fff;text-align:center}
h2{margin:12px 0 4px}img{width:100%;max-width:640px;border:3px solid #f97316;border-radius:8px;background:#000;min-height:180px}
.b{display:inline-block;margin:6px;padding:12px 18px;border:0;border-radius:8px;background:#f97316;color:#fff;font-size:16px}
select,input{font-size:16px;margin:6px}p{color:#9fb3c8;font-size:14px}</style></head><body>
<h2>ESP32-CAM test</h2><p id="i">loading...</p>
<img id="v"><br>
<button class="b" onclick="snap()">Photo</button>
<label>Flash <input type="range" min="0" max="255" value="0" onchange="fetch('/flash?v='+this.value)"></label><br>
<select onchange="fetch('/set?var=size&val='+this.value)">
<option value="5">QVGA 320x240</option><option value="8" selected>VGA 640x480</option><option value="9">SVGA 800x600</option></select>
<label><input type="checkbox" onchange="fetch('/set?var=vflip&val='+(this.checked?1:0))">Flip</label>
<label><input type="checkbox" onchange="fetch('/set?var=mirror&val='+(this.checked?1:0))">Mirror</label>
<p>If you see moving video, the ESP32-CAM works. Test 05 = PASS.</p>
<script>
const h=location.hostname;document.getElementById('v').src='http://'+h+':81/stream';
function snap(){window.open('/capture?'+Date.now())}
fetch('/info').then(r=>r.text()).then(t=>document.getElementById('i').textContent=t);
</script></body></html>)HTML";

static esp_err_t pageHandler(httpd_req_t* r) {
  httpd_resp_set_type(r, "text/html");
  return httpd_resp_send(r, PAGE, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t infoHandler(httpd_req_t* r) {
  char b[160];
  snprintf(b, sizeof b, "PSRAM: %s | free heap %u KB | %d phone(s) connected",
           psramFound() ? "yes" : "NO", ESP.getFreeHeap() / 1024, WiFi.softAPgetStationNum());
  return httpd_resp_send(r, b, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t captureHandler(httpd_req_t* r) {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) { httpd_resp_send_500(r); return ESP_FAIL; }
  httpd_resp_set_type(r, "image/jpeg");
  esp_err_t res = httpd_resp_send(r, (const char*)fb->buf, fb->len);
  esp_camera_fb_return(fb);
  return res;
}

static int queryInt(httpd_req_t* r, const char* key, int def) {
  char q[64], v[16];
  if (httpd_req_get_url_query_str(r, q, sizeof q) == ESP_OK &&
      httpd_query_key_value(q, key, v, sizeof v) == ESP_OK) return atoi(v);
  return def;
}

static esp_err_t flashHandler(httpd_req_t* r) {
  int v = constrain(queryInt(r, "v", 0), 0, 255);
  flashSet(v);
  Serial.printf("Flash LED = %d\n", v);
  return httpd_resp_send(r, "OK", 2);
}

static esp_err_t setHandler(httpd_req_t* r) {
  char q[64], var[16];
  if (httpd_req_get_url_query_str(r, q, sizeof q) != ESP_OK ||
      httpd_query_key_value(q, "var", var, sizeof var) != ESP_OK) return httpd_resp_send_404(r);
  int val = queryInt(r, "val", 0);
  sensor_t* s = esp_camera_sensor_get();
  if (!strcmp(var, "size"))   s->set_framesize(s, (framesize_t)val);
  if (!strcmp(var, "vflip"))  s->set_vflip(s, val);
  if (!strcmp(var, "mirror")) s->set_hmirror(s, val);
  Serial.printf("Camera %s = %d\n", var, val);
  return httpd_resp_send(r, "OK", 2);
}

#define BOUNDARY "frame"
static esp_err_t streamHandler(httpd_req_t* r) {
  httpd_resp_set_type(r, "multipart/x-mixed-replace;boundary=" BOUNDARY);
  httpd_resp_set_hdr(r, "Access-Control-Allow-Origin", "*");
  Serial.println("Video stream started");
  char hdr[80];
  uint32_t frames = 0, t0 = millis();
  while (true) {
    camera_fb_t* fb = esp_camera_fb_get();
    if (!fb) { Serial.println("  [FAIL] frame capture failed"); return ESP_FAIL; }
    int n = snprintf(hdr, sizeof hdr, "\r\n--" BOUNDARY "\r\nContent-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n", fb->len);
    esp_err_t res = httpd_resp_send_chunk(r, hdr, n);
    if (res == ESP_OK) res = httpd_resp_send_chunk(r, (const char*)fb->buf, fb->len);
    esp_camera_fb_return(fb);
    if (res != ESP_OK) break;                      // phone closed the page
    if (++frames % 50 == 0) {
      Serial.printf("Stream: %.1f fps\n", 50000.0f / (millis() - t0));
      t0 = millis();
    }
  }
  Serial.println("Video stream stopped");
  return ESP_OK;
}

void startServers() {
  httpd_config_t cfg = HTTPD_DEFAULT_CONFIG();
  cfg.server_port = 80; cfg.ctrl_port = 32768;
  httpd_uri_t u[] = {
    {"/",        HTTP_GET, pageHandler,    NULL},
    {"/info",    HTTP_GET, infoHandler,    NULL},
    {"/capture", HTTP_GET, captureHandler, NULL},
    {"/flash",   HTTP_GET, flashHandler,   NULL},
    {"/set",     HTTP_GET, setHandler,     NULL},
  };
  if (httpd_start(&webServer, &cfg) == ESP_OK)
    for (auto& x : u) httpd_register_uri_handler(webServer, &x);

  cfg.server_port = 81; cfg.ctrl_port = 32769;
  httpd_uri_t s = {"/stream", HTTP_GET, streamHandler, NULL};
  if (httpd_start(&streamServer, &cfg) == ESP_OK) httpd_register_uri_handler(streamServer, &s);
}

// ----------------------------------------------------------------- main -----
void setup() {
  Serial.begin(115200);
  delay(300);
  pinMode(RED_LED, OUTPUT); digitalWrite(RED_LED, HIGH);
  Serial.println("\n\n=== TEST 05 : ESP32-CAM only ===");

  Serial.printf("  [ OK ] Board booted, CPU %d MHz\n", getCpuFrequencyMhz());
  if (psramFound()) Serial.printf("  [ OK ] PSRAM %u KB\n", ESP.getPsramSize() / 1024);
  else              Serial.println("  [WARN] No PSRAM -> low resolution only (check board type)");

  flashInit();
  Serial.println("  ...    Flash LED blink test");
  for (int i = 0; i < 2; i++) { flashSet(40); delay(150); flashSet(0); delay(150); }

  bool camOk = cameraInit();

  bool joined = false;
  if (strlen(WIFI_SSID) > 0) {
    Serial.printf("  ...    Joining WiFi \"%s\"", WIFI_SSID);
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    for (int i = 0; i < 40 && WiFi.status() != WL_CONNECTED; i++) { delay(250); Serial.print('.'); }
    joined = WiFi.status() == WL_CONNECTED;
    Serial.println();
    if (joined) {
      Serial.printf("  [ OK ] Connected, signal %d dBm\n", WiFi.RSSI());
      Serial.printf("         Open  http://%s  in a browser on the same network\n", WiFi.localIP().toString().c_str());
    } else Serial.println("  [WARN] Could not join (wrong name/password, or 5 GHz only). Using own WiFi.");
  }
  if (!joined) {
    WiFi.mode(WIFI_AP);
    WiFi.softAP(AP_SSID, AP_PASS);
    Serial.printf("  [ OK ] WiFi \"%s\"  password \"%s\"\n", AP_SSID, AP_PASS);
    Serial.printf("         Open  http://%s  on your phone or PC\n", WiFi.softAPIP().toString().c_str());
  }
  WiFi.setSleep(false);

  if (camOk) startServers();
  Serial.println(camOk ? "Ready." : "Camera FAILED: fix it and press RST.");
}

void loop() {
  // red LED: slow blink = waiting, solid = device connected (or WiFi joined)
  static uint32_t t = 0; static int last = -1;
  int n = (WiFi.getMode() == WIFI_AP) ? WiFi.softAPgetStationNum() : (WiFi.status() == WL_CONNECTED);
  if (n != last) { Serial.printf(WiFi.getMode() == WIFI_AP ? "Devices connected: %d\n" : "WiFi link: %d\n", n); last = n; }
  if (n > 0) digitalWrite(RED_LED, LOW);
  else if (millis() - t > 500) { t = millis(); digitalWrite(RED_LED, !digitalRead(RED_LED)); }
  delay(20);
}
