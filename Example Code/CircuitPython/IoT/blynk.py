################################################################################
# Example for Blynk.
# Showing the status of virtual pin V0 on LED GP0.
# Send the status of push button GP20 to virtual pin V1.
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
import digitalio
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
API_URL = "http://blynk-cloud.com"

# Initialize LED and button.
led = digitalio.DigitalInOut(board.GP0)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP20)
button.direction = digitalio.Direction.INPUT

# Initialize UART connection to the ESP8266 WiFi Module.
RX = board.GP17
TX = board.GP16
uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.

esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)
requests.set_socket(socket, esp)

print("Resetting ESP module")
esp.soft_reset()

value_v0 = None

while True:
    try:
        # Make sure WiFi is connected.
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        
        # Reading Blynk virtual pin V0.
        pin = "V0"
        get_url = API_URL + "/" + secrets["blynk_auth_token"] + "/get/" + pin
        r = requests.get(get_url)
        value = int(r.text[2:-2])
        
        if value_v0 is None or value_v0 != value:
            value_v0 = value
            led.value = value
            print("V0:", value_v0)
            
        # Writting Blynk virtual pin V1.
        pin = "V1"
        value = not button.value  # Button is active low.
        get_url = API_URL + "/" + secrets["blynk_auth_token"] + "/update/" + pin + "?value=" + str(value)
        r = requests.get(get_url)

    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed, retrying\n", e)

