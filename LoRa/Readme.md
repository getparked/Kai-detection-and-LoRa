To set up the Arduino IDE follow steps 1 -> 4

1. Additional Boards Manager URL: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

2. Boards Manager Libraries
   Install "esp32 by Espressif"

3. Library Manager
  Install "Heltec ESP32 Dev-Boards"
  "TTN_esp32"

4. Tools
   Set LoRaWAN Region to US915

Once the IDE is setup connect to the LoRa and select it in the board select dropdown
Upload this code onto the LoRa

Disconnect the LoRa from the programming cable!!!

Also, connect Pi pins to Lora Pins (Pi -> Lora)
(5V -> 5V)
(GND -> GND)
(14 -> 22)
(15 -> 23)

Next, follow the instructions in /RaspberryPi

