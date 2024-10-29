#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

char ssid[] = "please";  // Enter your WIFI SSID
char pass[] = "00000000";  // Enter your WIFI Password

DHT dht(D4, DHT22); // DHT22 sensor connected to D4
unsigned long previousMillis = 0; // will store last time update occurred
const long interval = 1000; // interval at which to update (milliseconds)

// Define component pins
#define soil A0         // Soil Moisture Sensor
#define PIR D5          // PIR Motion Sensor
#define RELAY_PIN_1 D3  // Relay for the water pump

// URLs for PHP scripts
const char* server = "http://192.168.188.96/plant_monitoring_system";

// Variables for state management
int relay1State = HIGH; // Relay state (HIGH means off for active low relay)

void setup() {
  Serial.begin(9600);
  pinMode(PIR, INPUT);
  pinMode(RELAY_PIN_1, OUTPUT);
  digitalWrite(RELAY_PIN_1, relay1State); // Initialize relay as off (HIGH for active low relay)

  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.println("Connected to WiFi");
  dht.begin();
}

void DHT22sensor() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    return;
  }

  Serial.print("Temperature: ");
  Serial.println(t);
  Serial.print("Humidity: ");
  Serial.println(h);

  String url = String(server) + "/update_sensor_data.php?temperature=" + String(t) + "&humidity=" + String(h);

  WiFiClient client;
  HTTPClient http;
  http.begin(client, url); // Use WiFiClient instance and URL
  int httpCode = http.GET();
  http.end();
}

void soilMoistureSensor() {
  int value = analogRead(soil);
  value = map(value, 0, 1024, 0, 100);
  value = ((value - 100) * -1) * 1.2;

  Serial.print("Soil Moisture: ");
  Serial.println(value);

  String url = String(server) + "/update_sensor_data.php?soil_moisture=" + String(value);

  WiFiClient client;
  HTTPClient http;
  http.begin(client, url); // Use WiFiClient instance and URL
  int httpCode = http.GET();
  http.end();
}

void fetchAndPrintControlCommands() {
    String url = String(server) + "/get_button_state.php";
    Serial.println("Fetching button states from: " + url);

    WiFiClient client;
    HTTPClient http;
    http.begin(client, url); // Use WiFiClient instance and URL
    int httpCode = http.GET();
    if (httpCode > 0) {
        String payload = http.getString();
        Serial.println("Received payload: " + payload);

        // Parse JSON response
        DynamicJsonDocument doc(1024);
        DeserializationError error = deserializeJson(doc, payload);
        if (error) {
            Serial.print("deserializeJson() failed: ");
            Serial.println(error.f_str());
            return;
        }

        // Extract relay state
        String relayState = doc["RELAY"].as<String>();
        Serial.println("Relay State: " + relayState);

        // Update relay state based on the fetched button state from the database
        if (relayState == "ON") {
            relay1State = LOW;  // Relay on (active low)
            digitalWrite(RELAY_PIN_1, relay1State);
            Serial.println("Pump (Relay) ON");
        } else {
            relay1State = HIGH;  // Relay off
            digitalWrite(RELAY_PIN_1, relay1State);
            Serial.println("Pump (Relay) OFF");
        }

    } else {
        Serial.println("Error on HTTP request");
    }
    http.end();
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    soilMoistureSensor();
    DHT22sensor();
    fetchAndPrintControlCommands();
  }
}
