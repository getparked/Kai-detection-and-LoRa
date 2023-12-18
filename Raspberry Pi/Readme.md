# Raspberry Pi Setup
1. Ensure that the LoRa board is connected by following the steps in /LoRa
2. Run the script ./TTN setup/piToTNNSetup.py then press RST on the LoRa board
3. "Connection to TTN" will print followed by "." until a connection happens
4. Once a connection is made the serial monitor will display "Connected to TTN!", "Sending data", (data), "data sent", (data)
5. You can then send test data using ./TTN setup/piToTTNData.py
6. Either check The Things Network console or the app for data updates to ensure a connection
7. Once the connection is made you can then run ./Object Detection/detect_custom_presetImage.py
8. This code uses a predefined input image and runs it through the model that is inside the same folder
9. After running the code it will print the data that is sent to the LoRa and the detection output will be displayed, this will repeat every 30 seconds as it did for the presentation just with the same photo
