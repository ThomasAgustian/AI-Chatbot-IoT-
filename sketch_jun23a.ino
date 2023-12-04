#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "SHELBY KONTRAKAN LTD";
const char* password = "Shelbyuhuyuhuy";

ESP8266WebServer server(80);

#define lightPin D1  // Pin connected with LED

void handleRoot() {
  server.send(200, "text/html", "<h1>NodeMCU Web Server</h1><p>Klik <a href=\"/light/on\">here</a> for turn on the LED.</p><p>Klik <a href=\"/light/off\">here</a> For turn off the LED.</p>");
}

void handleLightOn() {
  digitalWrite(lightPin, LOW); // LED ON
  server.send(200, "text/plain", "Light turned on");
}

void handleLightOff() {
  digitalWrite(lightPin, HIGH); // LED OFF
  server.send(200, "text/plain", "Light turned off");
}

void setup() {
  pinMode(lightPin, OUTPUT); 

  WiFi.begin(ssid, password); 

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/light/on", handleLightOn);
  server.on("/light/off", handleLightOff);

  server.begin();
}

void loop() {
  server.handleClient();
}
