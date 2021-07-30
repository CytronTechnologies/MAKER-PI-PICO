# Examples for Internet of Things (IoT)
This folder shows a few examples for IoT applications.

## Required Hardware:
1. [Cytron Maker Pi Pico](https://www.cytron.io/p-maker-pi-pico) or [Cytron Maker Pi RP2040](https://www.cytron.io/p-maker-pi-rp2040)
2. ESP8266 WiFi module (eg: ESP-01, ESP-12F, WROOM-02) with Espressif AT Firmware v2.2.0 and above.
   You may download the firmware from the links below to update on your own.
   - [ESP-01 AT Firmware v2.2.0](https://drive.google.com/file/d/1q4QLJlIWHVQznaWsVvPev9ZW9vRHr1F8/view?usp=sharing)
   - [Cytron ESP8266 Grove WiFi Module (ESP-12F) AT Firmware v2.2.0](https://drive.google.com/file/d/1ZBZET0IN_RHkkObpaD7v-1-tqtQXbiUM/view?usp=sharing)

## Dependencies:
We've already included the following dependencies in the lib folder:
- adafruit_requests
- adafruit_espatcontrol

For latest version, you may download it from https://circuitpython.org/libraries

## Instructions:
1. Copy the lib folder to the CIRCUITPY device.
2. Modify the keys in secrets.py and copy it to the CIRCUITPY device.
3. Make sure the UART pins are defined correctly in the example code according to your hardware.
