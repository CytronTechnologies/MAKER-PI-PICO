################################################################################
# Example for Adafruit IO.
# - Control on-board LED through "led" feed.
# - Reads Pico internal CPU temperature and sends it to Adafruit IO
#   through "temperature" feed.
#
# Hardware:
# - Maker Pi Pico or Maker Pi RP2040
# - ESP8266 WiFi module with Espressif AT Firmware v2.2.0 and above.
#
# Dependencies:
# - adafruit_espatcontrol
# - adafruit_requests.mpy
# - adafruit_io
# - adafruit_minimqtt
#
# Instructions:
# - Setup Adafruit IO as shown here
#   https://learn.adafruit.com/quickstart-rp2040-pico-with-wifi-and-circuitpython/usage-with-adafruit-io
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
from microcontroller import cpu
import board
import digitalio
import busio
import adafruit_requests as requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
from adafruit_espatcontrol import adafruit_espatcontrol_wifimanager
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("All secret keys are kept in secrets.py, please add them there!")
    raise

# Initialize UART connection to the ESP8266 WiFi Module.
RX = board.GP17
TX = board.GP16
uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.

esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)

wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets)

# Initialize LED and button.
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# Define callback functions which will be called when certain events happen.
# pylint: disable=unused-argument
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    print("Connected to Adafruit IO! ")

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

# pylint: disable=unused-argument
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")

def on_led_msg(client, topic, message):
    # Method called whenever user/feeds/led has a new value
    print("New message on topic {0}: {1} ".format(topic, message))
    if message == "ON":
        led.value = True
    elif message == "OFF":
        led.value = False
    else:
        print("Unexpected message on LED feed.")

# Connect to WiFi
print("Connecting to WiFi...")
wifi.connect()
print("Connected!")

MQTT.set_socket(socket, esp)

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    username=secrets["aio_username"],
    password=secrets["aio_key"],
)

# Initialize an Adafruit IO MQTT Client
io = IO_MQTT(mqtt_client)

# Connect the callback methods defined above to Adafruit IO
io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe

# Set up a callback for the led feed
io.add_feed_callback("led", on_led_msg)

# Connect to Adafruit IO
print("Connecting to Adafruit IO...")
io.connect()

# Subscribe to all messages on the led feed
io.subscribe("led")

prv_refresh_time = 0.0
while True:
    # Poll for incoming messages
    try:
        io.loop()
    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset()
        io.reconnect()
        continue
    # Send a new temperature reading to IO every 30 seconds
    if (time.monotonic() - prv_refresh_time) > 30:
        # take the cpu's temperature
        cpu_temp = cpu.temperature
        # truncate to two decimal points
        cpu_temp = str(cpu_temp)[:5]
        print("CPU temperature is %s degrees C" % cpu_temp)
        # publish it to io
        print("Publishing %s to temperature feed..." % cpu_temp)
        io.publish("temperature", cpu_temp)
        print("Published!")
        prv_refresh_time = time.monotonic()
