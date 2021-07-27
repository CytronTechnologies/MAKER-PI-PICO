################################################################################
# Sending data to Thingspeak every 20 seconds.
#
# Hardware:
# - Maker Pi Pico or Maker Pi RP2040
# - ESP8266 WiFi module with Espressif AT Firmware v2.2.0 and above.
#
# Dependencies:
# - adafruit_requests
# - adafruit_espatcontrol
#
# Instructions:
# - Copy the lib folder to the CIRCUITPY device.
# - Modify the keys in secrets.py and copy to the CIRCUITPY device.
# - Make sure the UART pins are defined correctly according to your hardware.
#
#
# Author: Cytron Technologies
# Website: www.cytron.io
# Email: support@cytron.io
################################################################################

import time
import board
import busio
import adafruit_requests as requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("All secret keys are kept in secrets.py, please add them there!")
    raise

# Thingspeak API url.
API_URL = "http://api.thingspeak.com"


# Initialize UART connection to the ESP8266 WiFi Module.
RX = board.GP17
TX = board.GP16
uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.

esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)
requests.set_socket(socket, esp)

print("Resetting ESP module")
esp.soft_reset()



value = 1

while True:
    try:
        print("\nChecking WiFi connection...")
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
            
        print("\nUpdating Thingspeak...")
        get_url = API_URL + "/update?api_key=" + secrets["thingspeak_write_api_key"] + "&field1=" + str(value)
        r = requests.get(get_url)
        print("Value:", value)
        print("Data Count:", r.text)
        print("OK")

        value += 1
        time.sleep(20)  # Free version of Thingspeak only allows one update every 20 seconds.
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed, retrying\n", e)
