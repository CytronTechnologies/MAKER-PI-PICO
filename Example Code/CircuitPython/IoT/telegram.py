################################################################################
# Sending Telegram message using Telegram Bot.
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

# Telegram API url.
API_URL = "https://api.telegram.org"


# Initialize UART connection to the ESP8266 WiFi Module.
RX = board.GP17
TX = board.GP16
uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.

esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)
requests.set_socket(socket, esp)

print("Resetting ESP module")
esp.soft_reset()

while True:
    try:
        print("\nChecking WiFi connection...")
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        
        print("\nSending Telegram message...")
        message = "Hello World from Circuitpython :)"
        get_url = API_URL
        get_url += "/bot"
        get_url += secrets["telegram_bot_token"]
        get_url += "/sendMessage?chat_id="
        get_url += secrets["telegram_chat_id"]
        get_url += "&text="
        get_url += message
        r = requests.get(get_url)
        print("OK")
        break
        
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed, retrying\n", e)
