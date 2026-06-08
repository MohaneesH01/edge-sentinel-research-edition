#include <Adafruit_INA219.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <WiFi.h>

#if __has_include("config.h")
#include "config.h"
#else
#include "config.example.h"
#endif

#define DHT_PIN 4
#define DHT_TYPE DHT22

Adafruit_INA219 ina219;
DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

unsigned long lastPublishMs = 0;
const unsigned long publishIntervalMs = 3000;

void connectWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void connectMqtt() {
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  while (!mqttClient.connected()) {
    mqttClient.connect("edge-sentinel-esp32");
    delay(500);
  }
}

const char* classifyFault(float voltage, float current, float temperature) {
  if (voltage < 0 || current < 0 || temperature < -20.0) {
    return "sensor_failure";
  }
  if (voltage < 1.0 && current < 0.05) {
    return "open_circuit";
  }
  if (temperature >= 45.0) {
    return "temperature_anomaly";
  }
  if (current < 0.35) {
    return "partial_shading";
  }
  if (current > 1.5) {
    return "current_deviation";
  }
  return "normal";
}

int faultClassForLabel(const char* label) {
  if (strcmp(label, "open_circuit") == 0) return 1;
  if (strcmp(label, "partial_shading") == 0) return 2;
  if (strcmp(label, "temperature_anomaly") == 0) return 3;
  if (strcmp(label, "current_deviation") == 0) return 4;
  if (strcmp(label, "sensor_failure") == 0) return 5;
  return 0;
}

void publishTelemetry() {
  float busVoltage = ina219.getBusVoltage_V();
  float currentA = ina219.getCurrent_mA() / 1000.0;
  float temperatureC = dht.readTemperature();

  if (isnan(temperatureC)) {
    temperatureC = -99.0;
  }

  float powerW = busVoltage * currentA;
  const char* faultLabel = classifyFault(busVoltage, currentA, temperatureC);
  int faultClass = faultClassForLabel(faultLabel);

  char payload[256];
  snprintf(
    payload,
    sizeof(payload),
    "{\"voltage\":%.3f,\"current\":%.3f,\"temperature\":%.2f,\"power\":%.3f,\"fault_class\":%d,\"fault_label\":\"%s\"}",
    busVoltage,
    currentA,
    temperatureC,
    powerW,
    faultClass,
    faultLabel
  );

  mqttClient.publish(MQTT_TOPIC, payload);
}

void setup() {
  Serial.begin(115200);
  ina219.begin();
  dht.begin();
  connectWifi();
  connectMqtt();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWifi();
  }
  if (!mqttClient.connected()) {
    connectMqtt();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublishMs >= publishIntervalMs) {
    lastPublishMs = now;
    publishTelemetry();
  }
}
