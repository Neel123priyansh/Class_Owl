#include "esp_camera.h"
#include <WiFi.h>

const char* ssid = "moto";
const char* password = "tere9876";

void startCameraServer();

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println(WiFi.localIP());

  camera_config_t config;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_camera_init(&config);
  startCameraServer();
}

void loop() {}
