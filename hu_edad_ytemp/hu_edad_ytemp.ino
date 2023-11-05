#include <WiFi.h>
#include <HTTPClient.h>
#include "DHTesp.h"

#define DHTPIN 5 // Cambia este número al pin GPIO al que conectaste el pin de datos del sensor

const char* ssid = "Redmi 9";
const char* password = "12345678";
const char* apiEndpoint = "http://192.168.33.237:5000/api"; // Agrega el esquema "http://" y asegúrate de que la dirección y el puerto sean correctos

DHTesp dht;
unsigned long previousMillis = 0;

void setup() {
  Serial.begin(115200);
  dht.setup(DHTPIN, DHTesp::DHT11);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a la red WiFi");
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= 5000) {
    sendDataToAPI();
    previousMillis = currentMillis;
  }
}

void sendDataToAPI() {
  float temperature = dht.getTemperature();
  float humidity = dht.getHumidity();

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Agrega el esquema "http://" a la URL del punto final
    http.begin(apiEndpoint);

    // Formatea los números con 2 lugares decimales
    String jsonPayload = "{\"temperature\": " + String(temperature, 2) + ", \"humidity\": " + String(humidity, 2) + "}";

    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(jsonPayload);

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Respuesta de la API: " + payload);
    } else {
      Serial.println("Error al enviar los datos a la API");
    }

    http.end();
  }
}
