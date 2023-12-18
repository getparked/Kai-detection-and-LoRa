// Run piToTTNpi.py on the Raspberry pi and then press RST on the LoRa board

#include "heltec.h"
#include "Arduino.h"
#include <TTN_esp32.h>

//get-parked-lot-0 TTN console
const char* devEui = "70B3D57ED0061863";
const char* appEui = "CA0011C0113F0000";
const char* appKey = "690D232BA3C3E2A2A2B3DBE994EEE002";

TTN_esp32 ttn;

void setup() {
  //Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, 22, 23);
  delay(1000);
  //Serial.println("Starting");

  //connect to the things network
  ttn.begin();
  ttn.join(devEui, appEui, appKey);
  //Serial.print("Joining TTN ");
  Serial1.print("Joining TTN\n");
  while (!ttn.isJoined()){
    Serial1.print(".\n");
    //Serial.print(".");
    delay(1000);
  }
  //Serial.println("\njoined!");
  Serial1.print("Connected to TTN!\n");
  ttn.showStatus();
}

int count = 0;
bool update = false;
String received = "";
byte data[24]; // count how many parking stalls and then do count/8 and round up to larger 8 int

void loop() {
  if(Serial1.available()){
    char input = Serial1.read();
    if (input == ','){
      //Serial.println(received);
      data[count] = received.toInt();
      count++;
      received = "";
    } else if (input == ';'){
      update = true;
    } else {
      received += input;
    }
  }

  if (update == true){
    // for(int i = 0; i < sizeof(data); i++){
    //   Serial.print(data[i]);
    //   Serial.print(" ");
    // }
    ttn.sendBytes(data, sizeof(data));

    update = false;
    count = 0;
    for(int i = 0; i < sizeof(data); i++){
      Serial1.print(data[i]);
      Serial1.print(" ");
    }
    Serial1.print(" sent to things network\n");
  }

}
