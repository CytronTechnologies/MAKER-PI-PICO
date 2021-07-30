# Examples for Internet of Things (IoT)
This folder shows a few examples for IoT applications.

## Required Hardware:
1. [Cytron Maker Pi Pico](https://www.cytron.io/p-maker-pi-pico) or [Cytron Maker Pi RP2040](https://www.cytron.io/p-maker-pi-rp2040)
2. ESP8266 WiFi module (eg: ESP-01, ESP-12F, WROOM-02) with Espressif AT Firmware v2.2.0 and above. Follow [these steps](https://www.elec-cafe.com/esp8266-esp-01-firmware-update/) to update the firmware of the ESP-01. Latest firmware is provided as below:
   - [ESP-01 AT Firmware v2.2.0](https://drive.google.com/file/d/1q4QLJlIWHVQznaWsVvPev9ZW9vRHr1F8/view?usp=sharing)
   - [Cytron ESP8266 Grove WiFi Module (ESP-12F) AT Firmware v2.2.0](https://drive.google.com/file/d/1ZBZET0IN_RHkkObpaD7v-1-tqtQXbiUM/view?usp=sharing)

## Dependencies:
We've already included the following dependencies in the lib folder:
- adafruit_espatcontrol
- adafruit_requests.mpy
- adafruit_minimqtt
- adafruit_io

For latest version, you may download it from https://circuitpython.org/libraries

## Instructions:
1. Copy the lib folder to the CIRCUITPY device.
2. Modify the keys in secrets.py and copy it to the CIRCUITPY device.
3. Make sure the UART pins are defined correctly in the example code according to your hardware.

## Examples:
### Blynk
This example does two things:
1. Control LED GP0 on Maker Pi Pico using the Button Widget in the Blynk App via virtual pin V0.
2. Use the Button GP20 on Maker Pi Pico to control the LED Widget in the Blynk App via virtual pin V1.

This example requires the ssid, password and blynk_auth_token to be specified in the secrets.py.<br>
Follow [this video](https://youtu.be/UBQCaxfeBKY?t=93) to learn how to setup the Blynk app and get your auth token (Please ignore the part about Arduino IDE).
