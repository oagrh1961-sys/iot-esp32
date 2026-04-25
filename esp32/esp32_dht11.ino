#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include "credentials.h"

#define DHTPIN 4
#define DHTTYPE DHT11

const char* serverUrl = "http://<IP_SERVIDOR>:8000/datos";

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("Iniciando DHT11...");
  dht.begin();
  Serial.print("Conectando a WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
  Serial.print("IP local: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  delay(5000);
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();
  if (isnan(temperatura) || isnan(humedad)) {
    Serial.println("Error leyendo el DHT11");
    return;
  }
  Serial.println("----- DATOS DEL SENSOR -----");
  Serial.print("Temperatura: "); Serial.print(temperatura); Serial.println(" °C");
  Serial.print("Humedad: "); Serial.print(humedad); Serial.println(" %");
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    StaticJsonDocument<200> doc;
    doc["temperatura"] = temperatura;
    doc["humedad"] = humedad;
    doc["dispositivo"] = "ESP32-01";
    String jsonString;
    serializeJson(doc, jsonString);
    Serial.println("Enviando JSON al servidor...");
    Serial.println(jsonString);
    int httpCode = http.POST(jsonString);
    if (httpCode > 0) {
      Serial.print("Codigo HTTP: "); Serial.println(httpCode);
      Serial.println("Respuesta: "); Serial.println(http.getString());
    } else {
      Serial.print("Error en POST: "); Serial.println(httpCode);
    }
    http.end();
  }
  Serial.println("------ FIN DEL CICLO ------\n");
}
