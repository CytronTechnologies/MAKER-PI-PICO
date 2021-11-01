import pyRTOS
import board
import digitalio
import adafruit_dht
import analogio
import busio
import adafruit_ssd1306
import adafruit_requests as requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol

temp = 0.0
humidity = 0.0
air = 0.0
motion = 0
sound = 0

def DetectMotion(self):
    PIR = digitalio.DigitalInOut(board.GP1)
    PIR.direction = digitalio.Direction.INPUT
    global motion
    yield

    while True:
        if PIR.value:
            motion = 1
        yield [pyRTOS.timeout(0.1)]           # Delay in seconds (Other task can run)

def DetectSound(self):
    mic = digitalio.DigitalInOut(board.GP3)
    mic.direction = digitalio.Direction.INPUT
    global sound
    yield

    while True:
        if mic.value:
            sound = 1
        yield [pyRTOS.timeout(0.1)]           # Delay in seconds (Other task can run)

def ReadDHT11(self):
    dhtDevice = adafruit_dht.DHT11(board.GP5)
    global temp
    global humidity
    yield

    while True:
        try:
            temp = dhtDevice.temperature
            humidity = dhtDevice.humidity
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
        yield [pyRTOS.timeout(1)]           # Delay in seconds (Other task can run)

def AirQuality(self):
    airq = analogio.AnalogIn(board.A1)
    conv = 330 / (65535)
    global air
    yield

    while True:
        air = round((airq.value * conv), 2)
        yield [pyRTOS.timeout(0.2)]           # Delay in seconds (Other task can run)

def DisplayOLED(self):
    i2c = busio.I2C(board.GP9, board.GP8)
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
    global temp
    global humidity
    global air
    global motion
    global sound
    yield

    while True:
        oled.fill(0)

        oled.text('Temperature = ', 0, 0, 1)
        oled.text(str(temp), 90, 0, 1)
        oled.text('Humidity = ', 0, 25, 1)
        oled.text(str(humidity), 90, 25, 1)
        oled.text('Air Pollution = ', 0, 50, 1)
        oled.text(str(air), 90, 50, 1)

        oled.show()
        yield [pyRTOS.timeout(0.5)]           # Delay in seconds (Other task can run)

def SendData(self):
    global temp
    global humidity
    global air
    global motion
    global sound
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
    requests.set_socket(socket, esp)
    print("Resetting ESP module")
    esp.soft_reset()
    # Connect to WiFi
    print("Connecting to WiFi...")
    esp.connect(secrets)
    print("Connected!")
    yield

    while True:
        requests.get("https://blynk.cloud/external/api/update?token=" + secrets["blynk_auth_token"] + "&v0=" + str(temp))
        yield [pyRTOS.timeout(0.5)]           # Let other tasks run
        requests.get("https://blynk.cloud/external/api/update?token=" + secrets["blynk_auth_token"] + "&v1=" + str(humidity))
        yield [pyRTOS.timeout(0.5)]           # Let other tasks run
        requests.get("https://blynk.cloud/external/api/update?token=" + secrets["blynk_auth_token"] + "&v2=" + str(air))
        yield [pyRTOS.timeout(0.5)]           # Let other tasks run
        requests.get("https://blynk.cloud/external/api/update?token=" + secrets["blynk_auth_token"] + "&v3=" + str(motion))
        yield [pyRTOS.timeout(0.5)]           # Let other tasks run
        requests.get("https://blynk.cloud/external/api/update?token=" + secrets["blynk_auth_token"] + "&v4=" + str(sound))
        yield [pyRTOS.timeout(0.5)]           # Let other tasks run
        if motion:
            motion = 0
        if sound:
            sound = 0
        yield [pyRTOS.timeout(0.5)]           # Delay in seconds (Other task can run)

pyRTOS.add_task(pyRTOS.Task(DetectMotion))  # Add Tasks
pyRTOS.add_task(pyRTOS.Task(DetectSound))
pyRTOS.add_task(pyRTOS.Task(ReadDHT11))
pyRTOS.add_task(pyRTOS.Task(AirQuality))
pyRTOS.add_task(pyRTOS.Task(DisplayOLED))
pyRTOS.add_task(pyRTOS.Task(SendData))
pyRTOS.start()                              # Start pyRTOS
