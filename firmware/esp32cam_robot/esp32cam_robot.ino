/*
 * ============================================================================
 *  ROBOT CAR - ESP32-CAM "brain"   (camera + WiFi + phone web app)
 * ============================================================================
 *  - Creates WiFi network "RobotCar" (password 12345678)
 *  - Phone opens http://192.168.4.1       -> driver app (joystick, video, radar, lights)
 *  - PC opens    http://192.168.4.1/view  -> classroom viewer (big video, radar, live data)
 *  - Live video  : http://192.168.4.1:81/stream   (MJPEG, up to 3 viewers at once)
 *  - Controls    : WebSocket  ws://192.168.4.1/ws
 *  - Forwards drive commands to the Arduino UNO over serial,
 *    and forwards the UNO's ultrasonic data back to the phone (radar).
 *
 *  Board in Arduino IDE : "AI Thinker ESP32-CAM"   (esp32 by Espressif, 2.x or 3.x)
 *  Libraries            : none (everything is built into the ESP32 core)
 *
 *  Edit config.h for WiFi name/password and options.
 *  The web pages live in web/index.html (phone) and web/view.html (PC);
 *  run tools/build_ui.py after editing them to regenerate index_html.h / view_html.h.
 * ============================================================================
 */

#include <Arduino.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include "esp_camera.h"
#include "esp_http_server.h"
#include <lwip/sockets.h>
#include <netinet/tcp.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

#include "config.h"
#include "camera_pins.h"
#include "index_html.h"
#include "view_html.h"

// ------------------------------------------------------------- globals -----
HardwareSerial Link(1);                 // UART1: TX=IO14 -> UNO D3, RX=IO15 <- UNO D2

static httpd_handle_t ctrlServer   = NULL;  // port 80 : page, websocket, status
static httpd_handle_t streamServer = NULL;  // port 81 : video

// Values written by the web server task, read by loop()
static volatile int16_t  driveL = 0, driveR = 0;
static volatile uint32_t lastDriveMs = 0;
static volatile bool     driveDirty = false;
static volatile int8_t   hornState = 0;
static volatile bool     hornDirty = false;
static volatile int8_t   songState = 0;
static volatile bool     songDirty = false;
static volatile bool     cfgDirty  = false;
static volatile int      cfgWarn = 100, cfgStop = 15, cfgBrake = 1, cfgAlways = 0, cfgMute = 0, cfgInvertDrive = 0;
static volatile uint8_t  camFlash = 0;     // white flash LED on the ESP32-CAM (0-255)
static volatile uint8_t  lightMode = 0;    // car headlights on the UNO: 0 off, 1 on, 2 hazard
static volatile bool     lightDirty = false;

// Who is connected: phones (drivers) and PC viewers. Each page says "R,phone" or "R,view".
#define MAX_CLIENTS 8
static int  clientFd[MAX_CLIENTS];
static char clientRole[MAX_CLIENTS];       // 'P' phone, 'V' viewer, 0 free

// Latest sensor report from the UNO (for /status)
static volatile int      lastAngle = 90, lastDist = 0, lastFlags = 0;
static volatile uint32_t lastUnoMs = 0;

static bool apMode = true;

// ====================================================== camera flash ======
// Use LEDC channel 7 (timer 3) so we do not disturb the camera clock (channel 0 / timer 0)
static void flashSet(uint8_t v) {
  camFlash = v;
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcWrite(FLASH_LED_PIN, v);
#else
  ledcWrite(7, v);
#endif
}

static void flashInit() {
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcAttachChannel(FLASH_LED_PIN, 5000, 8, 7);
#else
  ledcSetup(7, 5000, 8);
  ledcAttachPin(FLASH_LED_PIN, 7);
#endif
  flashSet(0);
}

// =========================================================== camera =======
static bool cameraOk = false;
static bool isSoftwareSensor = false;
static uint8_t softwareJpgQuality = 55; // Fast software JPEG (50-60 is 3x faster than 80, sharp image & high FPS)

static bool cameraInit() {
  camera_config_t c = {};
  c.ledc_channel = LEDC_CHANNEL_0;
  c.ledc_timer   = LEDC_TIMER_0;
  c.pin_d0 = Y2_GPIO_NUM;  c.pin_d1 = Y3_GPIO_NUM;  c.pin_d2 = Y4_GPIO_NUM;
  c.pin_d3 = Y5_GPIO_NUM;  c.pin_d4 = Y6_GPIO_NUM;  c.pin_d5 = Y7_GPIO_NUM;
  c.pin_d6 = Y8_GPIO_NUM;  c.pin_d7 = Y9_GPIO_NUM;
  c.pin_xclk  = XCLK_GPIO_NUM;
  c.pin_pclk  = PCLK_GPIO_NUM;
  c.pin_vsync = VSYNC_GPIO_NUM;
  c.pin_href  = HREF_GPIO_NUM;
  c.pin_sccb_sda = SIOD_GPIO_NUM;
  c.pin_sccb_scl = SIOC_GPIO_NUM;
  c.pin_pwdn  = PWDN_GPIO_NUM;
  c.pin_reset = RESET_GPIO_NUM;
  c.xclk_freq_hz = 20000000;
  c.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    c.frame_size   = CAM_FRAMESIZE;
    c.jpeg_quality = CAM_QUALITY;
    c.fb_count     = 2;
    c.fb_location  = CAMERA_FB_IN_PSRAM;
    c.grab_mode    = CAMERA_GRAB_LATEST;
  } else {
    c.frame_size   = FRAMESIZE_QVGA;
    c.jpeg_quality = 15;
    c.fb_count     = 1;
    c.fb_location  = CAMERA_FB_IN_DRAM;
    c.grab_mode    = CAMERA_GRAB_WHEN_EMPTY;
  }

  // Attempt 1: Standard hardware JPEG (OV2640, OV3660, OV5640)
  esp_err_t err = esp_camera_init(&c);

  // Attempt 2: If JPEG returned 0x106 (ESP_ERR_NOT_SUPPORTED), the sensor is a non-JPEG
  // model (e.g. GC2145, OV7670, GC0308). Switch to RGB565 with PSRAM double-buffering at 20MHz!
  if (err != ESP_OK) {
    Serial.printf("Camera init (JPEG) returned 0x%x. Retrying with RGB565 at 20MHz...\n", err);
    esp_camera_deinit();
    delay(50);
    c.pixel_format = PIXFORMAT_RGB565;
    c.frame_size   = FRAMESIZE_QVGA;
    if (psramFound()) {
      c.fb_count    = 2;
      c.fb_location = CAMERA_FB_IN_PSRAM;
      c.grab_mode   = CAMERA_GRAB_LATEST;
    } else {
      c.fb_count    = 1;
      c.fb_location = CAMERA_FB_IN_DRAM;
      c.grab_mode   = CAMERA_GRAB_WHEN_EMPTY;
    }
    c.xclk_freq_hz = 20000000;
    err = esp_camera_init(&c);
  }

  // Attempt 3: If 20MHz RGB565 failed, try 16MHz
  if (err != ESP_OK) {
    Serial.printf("Camera init (20MHz) returned 0x%x. Retrying at 16MHz...\n", err);
    esp_camera_deinit();
    delay(50);
    c.xclk_freq_hz = 16000000;
    err = esp_camera_init(&c);
  }

  // Attempt 4: Fallback to 10MHz
  if (err != ESP_OK) {
    Serial.printf("Camera init (16MHz) returned 0x%x. Retrying at 10MHz...\n", err);
    esp_camera_deinit();
    delay(50);
    c.xclk_freq_hz = 10000000;
    err = esp_camera_init(&c);
  }

  if (err != ESP_OK) {
    Serial.printf("Camera init FAILED 0x%x (check ribbon cable / board type)\n", err);
    cameraOk = false;
    return false;
  }

  sensor_t *s = esp_camera_sensor_get();
  if (s) {
    Serial.printf("Camera sensor detected! PID: 0x%02X\n", s->id.PID);
    // Identify if sensor requires software JPEG encoding (GC2145, OV7670, GC0308)
    isSoftwareSensor = (s->id.PID == 0x2145 || s->id.PID == 0x76 || s->id.PID == 0x9b || s->id.PID == 0x232a);
    if (isSoftwareSensor) {
      Serial.println("Non-JPEG sensor: using hardware double-buffer + accelerated software JPEG");
      s->set_framesize(s, FRAMESIZE_QVGA); // QVGA (320x240) ensures smooth 25-30 FPS!
    }
    s->set_vflip(s, CAM_VFLIP);
    s->set_hmirror(s, CAM_HMIRROR);
  }
  cameraOk = true;
  return true;
}

// ======================================================= video stream =====
#define PART_BOUNDARY "123456789000000000000987654321"
static const char *STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;

static volatile int streamViewers = 0;

static esp_err_t streamLoop(httpd_req_t *req) {
  if (!cameraOk) {
    httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Camera not initialized");
    return ESP_FAIL;
  }

  // Optimize TCP socket for immediate streaming flush without Nagle buffering
  int sockfd = httpd_req_to_sockfd(req);
  if (sockfd >= 0) {
    int nodelay = 1;
    setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &nodelay, sizeof(nodelay));
  }

  char partHdr[128];
  esp_err_t res = httpd_resp_set_type(req, STREAM_CONTENT_TYPE);
  if (res != ESP_OK) return res;
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  httpd_resp_set_hdr(req, "Cache-Control", "no-cache, no-store, must-revalidate");
  httpd_resp_set_hdr(req, "Pragma", "no-cache");

  while (true) {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) { Serial.println("Frame capture failed"); res = ESP_FAIL; break; }

    uint8_t *jpg_buf = NULL;
    size_t jpg_len = 0;
    bool free_jpg = false;

    if (fb->format == PIXFORMAT_JPEG) {
      jpg_buf = fb->buf;
      jpg_len = fb->len;
    } else {
      // Fast software conversion: softwareJpgQuality = 55 (3x-4x faster than 80, ~7KB JPEGs)
      bool converted = frame2jpg(fb, softwareJpgQuality, &jpg_buf, &jpg_len);
      free_jpg = true;
      if (!converted || !jpg_buf) {
        esp_camera_fb_return(fb);
        vTaskDelay(pdMS_TO_TICKS(5));
        continue;
      }
    }

    // Combine boundary and part header in one single chunk to cut TCP packets in half
    size_t hlen = snprintf(partHdr, sizeof(partHdr),
                           "\r\n--" PART_BOUNDARY "\r\nContent-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n",
                           (unsigned)jpg_len);
    res = httpd_resp_send_chunk(req, partHdr, hlen);
    if (res == ESP_OK) {
      res = httpd_resp_send_chunk(req, (const char *)jpg_buf, jpg_len);
    }

    if (free_jpg && jpg_buf) free(jpg_buf);
    esp_camera_fb_return(fb);

    if (res != ESP_OK) break;               // viewer closed the stream

    // Minimal task yield to let networking & WebSocket process without wasting frame time
    vTaskDelay(pdMS_TO_TICKS(1));
  }
  return res;
}

#if ESP_ARDUINO_VERSION_MAJOR >= 3
// Each viewer gets its own task, so the phone and the PC can watch at the same time
static void streamTask(void *arg) {
  httpd_req_t *req = (httpd_req_t *)arg;
  streamLoop(req);
  httpd_req_async_handler_complete(req);
  streamViewers--;
  vTaskDelete(NULL);
}

static esp_err_t streamHandler(httpd_req_t *req) {
  if (streamViewers >= 3) { httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "too many viewers"); return ESP_FAIL; }
  httpd_req_t *copy = NULL;
  if (httpd_req_async_handler_begin(req, &copy) != ESP_OK) return streamLoop(req);
  streamViewers++;
  // Pin stream task to Core 1 with 8KB stack so it runs on a dedicated 240MHz core parallel to WiFi on Core 0
  if (xTaskCreatePinnedToCore(streamTask, "stream", 8192, copy, 5, NULL, 1) != pdPASS) {
    streamViewers--;
    httpd_req_async_handler_complete(copy);
    return ESP_FAIL;
  }
  return ESP_OK;
}
#else
// ESP32 core 2.x: one viewer at a time
static esp_err_t streamHandler(httpd_req_t *req) { return streamLoop(req); }
#endif

static esp_err_t captureHandler(httpd_req_t *req) {
  if (!cameraOk) { httpd_resp_send_err(req, HTTPD_500_INTERNAL_SERVER_ERROR, "Camera not initialized"); return ESP_FAIL; }
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) { httpd_resp_send_500(req); return ESP_FAIL; }

  uint8_t *jpg_buf = NULL;
  size_t jpg_len = 0;
  bool free_jpg = false;

  if (fb->format == PIXFORMAT_JPEG) {
    jpg_buf = fb->buf;
    jpg_len = fb->len;
  } else {
    bool converted = frame2jpg(fb, 80, &jpg_buf, &jpg_len);
    free_jpg = true;
    if (!converted || !jpg_buf) {
      esp_camera_fb_return(fb);
      httpd_resp_send_500(req);
      return ESP_FAIL;
    }
  }

  httpd_resp_set_type(req, "image/jpeg");
  httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=robotcar.jpg");
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  esp_err_t res = httpd_resp_send(req, (const char *)jpg_buf, jpg_len);

  if (free_jpg && jpg_buf) free(jpg_buf);
  esp_camera_fb_return(fb);
  return res;
}

// ===================================================== camera settings ====
static void cameraSet(char cmd, int v) {
  sensor_t *s = esp_camera_sensor_get();
  if (!s) return;
  switch (cmd) {
    case 'F':
      if (v >= FRAMESIZE_QQVGA && v <= FRAMESIZE_UXGA) {
        // For non-JPEG sensors, prevent choosing sizes larger than CIF (400x296) to keep frame rate high
        if (isSoftwareSensor && v > FRAMESIZE_CIF) v = FRAMESIZE_QVGA;
        s->set_framesize(s, (framesize_t)v);
      }
      break;
    case 'Q':
      if (isSoftwareSensor) {
        softwareJpgQuality = constrain(v, 25, 85);
      } else {
        s->set_quality(s, constrain(v, 10, 63));
      }
      break;
    case 'V': s->set_vflip(s, v ? 1 : 0); break;
    case 'X': s->set_hmirror(s, v ? 1 : 0); break;
    case 'B': s->set_brightness(s, constrain(v, -2, 2)); break;
  }
}

// ==================================================== phone messages ======
// Parse one text message from the phone (see docs/05_PROTOCOL.md)
static void handlePhoneMessage(char *msg) {
  char cmd = msg[0];
  int a[6] = {0, 0, 0, 0, 0, 0};
  int n = 0;
  char *p = strchr(msg, ',');
  while (p && n < 6) { a[n++] = atoi(p + 1); p = strchr(p + 1, ','); }

  switch (cmd) {
    case 'M':
      if (n < 2) return;
      driveL = constrain(a[0], -255, 255);
      driveR = constrain(a[1], -255, 255);
      lastDriveMs = millis();
      driveDirty = true;
      break;
    case 'S':
      driveL = driveR = 0; lastDriveMs = millis(); driveDirty = true;
      songState = 0; songDirty = true;
      break;
    case 'H':
      hornState = (n >= 1 && a[0]) ? 1 : 0; hornDirty = true;
      if (hornState) { songState = 0; songDirty = true; }
      lastDriveMs = millis();
      break;
    case 'P':                               // play song / melody on the buzzer
      songState = (n >= 1 && a[0]) ? 1 : 0; songDirty = true;
      break;
    case 'C':
      if (n < 5) return;
      cfgWarn = a[0]; cfgStop = a[1]; cfgBrake = a[2]; cfgAlways = a[3]; cfgMute = a[4];
      if (n >= 6) cfgInvertDrive = a[5];
      cfgDirty = true;
      break;
    case 'L':                               // car headlights (on the UNO)
      if (n >= 1) { lightMode = constrain(a[0], 0, 2); lightDirty = true; }
      break;
    case 'K':                               // camera flash LED (on the ESP32-CAM)
      if (n >= 1) flashSet(constrain(a[0], 0, 255));
      break;
    case 'F': case 'Q': case 'V': case 'X': case 'B':
      if (n >= 1) cameraSet(cmd, a[0]);
      break;
  }
}

// ========================================================= websocket ======
static void setRole(int fd, char role) {
  int freeSlot = -1;
  for (int i = 0; i < MAX_CLIENTS; i++) {
    if (clientRole[i] && clientFd[i] == fd) { clientRole[i] = role; return; }
    if (!clientRole[i] && freeSlot < 0) freeSlot = i;
  }
  if (freeSlot >= 0) { clientFd[freeSlot] = fd; clientRole[freeSlot] = role; }
}

static esp_err_t wsHandler(httpd_req_t *req) {
  if (req->method == HTTP_GET) {
    Serial.println("Device connected (WebSocket)");
    setRole(httpd_req_to_sockfd(req), 'P');  // until the page says what it is
    return ESP_OK;                          // handshake done
  }
  httpd_ws_frame_t f;
  memset(&f, 0, sizeof(f));
  f.type = HTTPD_WS_TYPE_TEXT;
  esp_err_t r = httpd_ws_recv_frame(req, &f, 0);          // get length
  if (r != ESP_OK) return r;
  if (f.len == 0 || f.len > 120) return ESP_OK;
  uint8_t buf[128];
  f.payload = buf;
  r = httpd_ws_recv_frame(req, &f, f.len);
  if (r != ESP_OK) return r;
  buf[f.len] = 0;
  if (f.type != HTTPD_WS_TYPE_TEXT) return ESP_OK;
  if (buf[0] == 'R' && buf[1] == ',') { setRole(httpd_req_to_sockfd(req), buf[2] == 'v' ? 'V' : 'P'); return ESP_OK; }
  handlePhoneMessage((char *)buf);
  return ESP_OK;
}

struct WsJob {
  httpd_handle_t hd;
  int fd;
  size_t len;
  char data[64];
};

static void wsSendJob(void *arg) {
  WsJob *j = (WsJob *)arg;
  httpd_ws_frame_t f;
  memset(&f, 0, sizeof(f));
  f.type = HTTPD_WS_TYPE_TEXT;
  f.final = true;
  f.payload = (uint8_t *)j->data;
  f.len = j->len;
  httpd_ws_send_frame_async(j->hd, j->fd, &f);
  free(j);
}

// Send a text message to every connected device. Returns the number of devices.
// If viewers != NULL it also counts how many of them are PC viewers.
static int wsBroadcast(const char *text, int *viewers = NULL) {
  if (!ctrlServer) return 0;
  int fds[16];
  size_t count = 16;
  if (httpd_get_client_list(ctrlServer, &count, fds) != ESP_OK) return 0;
  int sent = 0;
  for (size_t i = 0; i < count; i++) {
    if (httpd_ws_get_fd_info(ctrlServer, fds[i]) != HTTPD_WS_CLIENT_WEBSOCKET) continue;
    sent++;
    if (viewers)
      for (int k = 0; k < MAX_CLIENTS; k++)
        if (clientRole[k] == 'V' && clientFd[k] == fds[i]) (*viewers)++;
    if (!text) continue;                    // just counting
    WsJob *j = (WsJob *)malloc(sizeof(WsJob));
    if (!j) continue;
    j->hd = ctrlServer;
    j->fd = fds[i];
    j->len = strnlen(text, sizeof(j->data) - 1);
    memcpy(j->data, text, j->len);
    if (httpd_queue_work(ctrlServer, wsSendJob, j) != ESP_OK) free(j);
  }
  return sent;
}

// Forget the roles of sockets that are gone
static void pruneRoles() {
  for (int k = 0; k < MAX_CLIENTS; k++)
    if (clientRole[k] && httpd_ws_get_fd_info(ctrlServer, clientFd[k]) != HTTPD_WS_CLIENT_WEBSOCKET) clientRole[k] = 0;
}

// ====================================================== HTTP handlers =====
static esp_err_t indexHandler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/html");
  httpd_resp_set_hdr(req, "Cache-Control", "no-cache");
  return httpd_resp_send(req, INDEX_HTML, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t viewHandler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/html");
  httpd_resp_set_hdr(req, "Cache-Control", "no-cache");
  return httpd_resp_send(req, VIEW_HTML, HTTPD_RESP_USE_STRLEN);
}

static esp_err_t statusHandler(httpd_req_t *req) {
  char json[220];
  sensor_t *s = esp_camera_sensor_get();
  snprintf(json, sizeof(json),
           "{\"dist\":%d,\"angle\":%d,\"flags\":%d,\"uno\":%s,\"rssi\":%d,"
           "\"camOk\":%s,\"framesize\":%d,\"quality\":%d,\"lights\":%d,\"flash\":%d,\"heap\":%u}",
           lastDist, lastAngle, lastFlags,
           (millis() - lastUnoMs < 1000) ? "true" : "false",
           apMode ? 0 : (int)WiFi.RSSI(),
           cameraOk ? "true" : "false",
           s ? s->status.framesize : -1, s ? s->status.quality : -1,
           (int)lightMode, (int)camFlash, (unsigned)ESP.getFreeHeap());
  httpd_resp_set_type(req, "application/json");
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  return httpd_resp_send(req, json, HTTPD_RESP_USE_STRLEN);
}

// Plain HTTP fallback:  /cmd?c=M,120,120   (same messages as the WebSocket)
static esp_err_t cmdHandler(httpd_req_t *req) {
  char query[96], val[80];
  if (httpd_req_get_url_query_str(req, query, sizeof(query)) == ESP_OK &&
      httpd_query_key_value(query, "c", val, sizeof(val)) == ESP_OK) {
    // undo URL encoding of ',' (%2C)
    char clean[80]; size_t o = 0;
    for (size_t i = 0; val[i] && o < sizeof(clean) - 1; i++) {
      if (val[i] == '%' && val[i + 1] == '2' && (val[i + 2] == 'C' || val[i + 2] == 'c')) { clean[o++] = ','; i += 2; }
      else clean[o++] = val[i];
    }
    clean[o] = 0;
    handlePhoneMessage(clean);
  }
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  return httpd_resp_send(req, "OK", 2);
}

static void startServers() {
  httpd_config_t cfg = HTTPD_DEFAULT_CONFIG();
  cfg.server_port = 80;
  cfg.max_uri_handlers = 8;
  cfg.max_open_sockets = 7;
  cfg.lru_purge_enable = false;      // Never purge active WebSocket sockets
  cfg.stack_size = 8192;             // Adequate stack for WebSocket frame operations

  httpd_uri_t uIndex  = { .uri = "/",       .method = HTTP_GET, .handler = indexHandler,   .user_ctx = NULL };
  httpd_uri_t uView   = { .uri = "/view",   .method = HTTP_GET, .handler = viewHandler,    .user_ctx = NULL };
  httpd_uri_t uStatus = { .uri = "/status", .method = HTTP_GET, .handler = statusHandler,  .user_ctx = NULL };
  httpd_uri_t uCmd    = { .uri = "/cmd",    .method = HTTP_GET, .handler = cmdHandler,     .user_ctx = NULL };
  httpd_uri_t uCap    = { .uri = "/capture",.method = HTTP_GET, .handler = captureHandler, .user_ctx = NULL };
  httpd_uri_t uWs;
  memset(&uWs, 0, sizeof(uWs));
  uWs.uri = "/ws";
  uWs.method = HTTP_GET;
  uWs.handler = wsHandler;
  uWs.is_websocket = true;

  if (httpd_start(&ctrlServer, &cfg) == ESP_OK) {
    httpd_register_uri_handler(ctrlServer, &uIndex);
    httpd_register_uri_handler(ctrlServer, &uView);
    httpd_register_uri_handler(ctrlServer, &uStatus);
    httpd_register_uri_handler(ctrlServer, &uCmd);
    httpd_register_uri_handler(ctrlServer, &uCap);
    httpd_register_uri_handler(ctrlServer, &uWs);
  } else {
    Serial.println("ERROR: control server did not start");
  }

  // Second server on port 81 for video, so streaming never blocks the controls
  httpd_config_t scfg = HTTPD_DEFAULT_CONFIG();
  scfg.server_port = 81;
  scfg.ctrl_port   = cfg.ctrl_port + 1;
  scfg.max_open_sockets = 4;
  httpd_uri_t uStream = { .uri = "/stream", .method = HTTP_GET, .handler = streamHandler, .user_ctx = NULL };
  if (httpd_start(&streamServer, &scfg) == ESP_OK) {
    httpd_register_uri_handler(streamServer, &uStream);
  } else {
    Serial.println("ERROR: stream server did not start");
  }
}

// ============================================================ WiFi ========
static void wifiStart() {
  WiFi.persistent(false);
  if (strlen(STA_SSID) > 0) {
    Serial.printf("Joining WiFi \"%s\" ", STA_SSID);
    WiFi.mode(WIFI_STA);
    WiFi.setTxPower(WIFI_POWER_15dBm);       // Reduce RF peak surges from 450mA to ~260mA
    WiFi.begin(STA_SSID, STA_PASSWORD);
    uint32_t t0 = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - t0 < 10000) { delay(250); Serial.print('.'); }
    Serial.println();
    if (WiFi.status() == WL_CONNECTED) {
      apMode = false;
      WiFi.setSleep(false);
      MDNS.begin("robotcar");
      Serial.printf("Connected. Open  http://%s   (or http://robotcar.local)\n",
                    WiFi.localIP().toString().c_str());
      return;
    }
    Serial.println("Could not join, starting own WiFi network instead");
  }
  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASSWORD, AP_CHANNEL, 0, 4);
  WiFi.setSleep(false);
  WiFi.setTxPower(WIFI_POWER_15dBm);         // Protect 5V rail against brownout reset loops
  apMode = true;
  Serial.printf("WiFi network \"%s\" / password \"%s\"\n", AP_SSID, AP_PASSWORD);
  Serial.printf("Phone: open  http://%s       PC viewer: http://%s/view\n",
                WiFi.softAPIP().toString().c_str(), WiFi.softAPIP().toString().c_str());
}

// ==================================================== UNO serial link =====
static char unoBuf[48];
static uint8_t unoLen = 0;

static void readUno() {
  static uint32_t lastUnoBroadcast = 0;
  static int prevFlags = -1;
  while (Link.available()) {
    char ch = Link.read();
    if (ch == '\r') continue;
    if (ch == '\n') {
      unoBuf[unoLen] = 0;
      if (unoLen > 2 && unoBuf[0] == 'D' && unoBuf[1] == ',') {
        int a = 90, d = 0, f = 0;
        if (sscanf(unoBuf, "D,%d,%d,%d", &a, &d, &f) == 3) {
          lastAngle = a; lastDist = d; lastFlags = f; lastUnoMs = millis();
          // Rate-limit sensor broadcasts over WebSocket to ~90-100ms unless flags change,
          // which avoids flooding the async WebSocket queue and dropping the socket
          if (f != prevFlags || millis() - lastUnoBroadcast >= 90) {
            lastUnoBroadcast = millis();
            prevFlags = f;
            wsBroadcast(unoBuf);                    // straight to the radar
          }
        }
      }
      unoLen = 0;
    } else if (unoLen < sizeof(unoBuf) - 1) {
      unoBuf[unoLen++] = ch;
    } else {
      unoLen = 0;
    }
  }
}

// Send one line to the UNO with an XOR checksum:  "M,120,-80*3F\n"
// (the UNO's SoftwareSerial can lose bytes while it is transmitting, so
//  the UNO drops any line whose checksum does not match)
static void linkSend(const char *fmt, ...) {
  char buf[48];
  va_list ap;
  va_start(ap, fmt);
  vsnprintf(buf, sizeof(buf), fmt, ap);
  va_end(ap);
  uint8_t cs = 0;
  for (const char *c = buf; *c; c++) cs ^= (uint8_t)*c;
  Link.printf("%s*%02X\n", buf, cs);
}

static void sendToUno() {
  static uint32_t lastBeat = 0, lastCfg = 0, lastLight = 0;
  uint32_t now = millis();

  // Phone went silent while driving -> stop
  if ((driveL || driveR || hornState) && now - lastDriveMs > PHONE_TIMEOUT_MS) {
    driveL = driveR = 0;
    hornState = 0;
    driveDirty = hornDirty = true;
    Serial.println("Phone timeout -> STOP");
  }

  if (driveDirty || now - lastBeat >= HEARTBEAT_MS) {
    driveDirty = false;
    lastBeat = now;
    linkSend("M,%d,%d", (int)driveL, (int)driveR);
  }
  if (hornDirty) {
    hornDirty = false;
    linkSend("H,%d", (int)hornState);
  }
  if (songDirty) {
    songDirty = false;
    linkSend("P,%d", (int)songState);
  }
  // Settings: on change, and every 3 s in case the UNO was reset
  if (cfgDirty || now - lastCfg >= 3000) {
    cfgDirty = false;
    lastCfg = now;
    linkSend("C,%d,%d,%d,%d,%d,%d", cfgWarn, cfgStop, cfgBrake, cfgAlways, cfgMute, cfgInvertDrive);
  }
  // Headlights: on change, and every 3 s in case the UNO was reset
  if (lightDirty || now - lastLight >= 3000) {
    lightDirty = false;
    lastLight = now;
    linkSend("L,%d", (int)lightMode);
  }
}

// =========================================================== SETUP ========
void setup() {
#if DISABLE_BROWNOUT
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
#endif
  // Drive flash LED pin LOW immediately so it does not flicker or leak power during boot
  pinMode(FLASH_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, LOW);
  flashInit();

  Serial.begin(115200);
  Serial.println("\n=== ROBOT CAR ESP32-CAM ===");

  pinMode(STATUS_LED_PIN, OUTPUT);
  digitalWrite(STATUS_LED_PIN, HIGH);        // off (active LOW)

  Link.begin(LINK_BAUD, SERIAL_8N1, LINK_RX_PIN, LINK_TX_PIN);
  linkSend("S");                             // make sure the car is stopped

  if (!cameraInit()) {
    // Keep running so the car can still be driven without video
    Serial.println("Continuing WITHOUT camera");
  }
  wifiStart();
  startServers();
  Serial.println("Ready.");
}

// ============================================================ LOOP ========
void loop() {
  readUno();
  sendToUno();

  // Live state for every screen (so the PC viewer and all phones stay in sync):
  // T,<left>,<right>,<lights>,<horn>,<flash>
  static uint32_t lastState = 0;
  if (millis() - lastState >= 250) {
    lastState = millis();
    char st[48];
    snprintf(st, sizeof(st), "T,%d,%d,%d,%d,%d", (int)driveL, (int)driveR, (int)lightMode, (int)hornState, (int)camFlash);
    wsBroadcast(st);
  }

  // I,<rssi>,<phones>,<uno ok>,<viewers>
  static uint32_t lastInfo = 0;
  if (millis() - lastInfo >= 2000) {
    lastInfo = millis();
    pruneRoles();
    int viewers = 0;
    int devices = wsBroadcast(NULL, &viewers);
    char msg[48];
    snprintf(msg, sizeof(msg), "I,%d,%d,%d,%d", apMode ? 0 : (int)WiFi.RSSI(), devices - viewers,
             (millis() - lastUnoMs < 1000) ? 1 : 0, viewers);
    wsBroadcast(msg);
    if (millis() - lastUnoMs > 2000) Serial.println("WARNING: no data from UNO (check wiring: UNO D2 -> divider -> IO15, IO14 -> UNO D3, common GND)");
  }

  // Status LED: blinking = waiting for a device, solid = phone or PC connected
  static uint32_t lastBlink = 0;
  static int phonesCached = 0;
  if (millis() - lastBlink >= 500) {
    lastBlink = millis();
    phonesCached = wsBroadcast(NULL);
    if (phonesCached) digitalWrite(STATUS_LED_PIN, LOW);
    else digitalWrite(STATUS_LED_PIN, !digitalRead(STATUS_LED_PIN));
  }

  delay(2);
}
