/*
 * Code used in autotargetting gun project
 * SEE https://www.youtube.com/watch?v=S3CwzkT6cK4
 * *
 * Feel free to use this code as you want
 *
 * @author Tomas Hromada
 * Contact: tomashromada1@gmail.com
 * GitHub: https://github.com/tomash1234
 */

#include <SPI.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Servo.h>

#define PACKET_MAX_SIZE 64
#define WIFI_SSID "wifi_name"
#define WIFI_PASSWORD "password"
#define LOCAL_PORT 8525 //port where the board will be receiving data from computer
#define KEY_PACKET 44

Servo servoA; //trigger servo
Servo servoB; //elevation angle
Servo servoC; //rotate servo | azimuth 
WiFiUDP Udp;
int ledPin = D3;


static void connectToWifi(const char* ssid, const char* password){
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  
  WiFi.begin(ssid, password); 
  int i = 0;
  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(1000);
    Serial.print(++i); Serial.print(' ');
    if(i > 10){
      Serial.println("Failed! No connection");  
      break;
    }
  }
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
}

void setup() {
    pinMode(ledPin, OUTPUT);  
    digitalWrite(ledPin, HIGH);
    Serial.begin(9600);
    servoA.attach(D6); 
    servoB.attach(D5); 
    servoC.attach(D7); 
    
    connectToWifi(WIFI_SSID, WIFI_PASSWORD);

    Udp.begin(LOCAL_PORT);

    servoA.write(130);
    servoB.write(90);
    servoC.write(90);
}

static void read_packets(){
  int request = 0;
  while(Udp.parsePacket()){ 
    unsigned char* receivedData = (byte*) malloc(PACKET_MAX_SIZE * sizeof(unsigned char));
    int len = Udp.read(receivedData, PACKET_MAX_SIZE);
    Serial.printf("Received %d\n", len);
    
    if(len >= 3){
      if(receivedData[0] == KEY_PACKET && receivedData[1] == KEY_PACKET && receivedData[2] == 0){
          servoA.write(150); // reload
      }else if(receivedData[0] == KEY_PACKET && receivedData[1] == KEY_PACKET && receivedData[2] == 64){
          servoA.write(70); //shoot
      }else if(receivedData[0] == KEY_PACKET && receivedData[1] == 88){
          servoB.write((int)receivedData[2]);
      }else if(receivedData[0] == KEY_PACKET && receivedData[1] == 120){
          servoC.write((int)receivedData[2]); //rotate azimuth
      }else if(receivedData[0] == KEY_PACKET && receivedData[1] == 140){
        if(receivedData[2]>50){
          digitalWrite(ledPin, HIGH);
        }else{
          digitalWrite(ledPin, LOW);
        }
      }
    }
    free(receivedData);
  }
}

void loop() {
  read_packets();
}
