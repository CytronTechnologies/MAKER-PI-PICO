# SPDX-FileCopyrightText: 2018 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_espatcontrol.adafruit_espatcontrol`
====================================================

Use the ESP AT command sent to communicate with the Interwebs.
Its slow, but works to get data into CircuitPython

Command set:
https://www.espressif.com/sites/default/files/documentation/4a-esp8266_at_instruction_set_en.pdf

Examples:
https://www.espressif.com/sites/default/files/documentation/4b-esp8266_at_command_examples_en.pdf

* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

* Adafruit `ESP8266 Huzzah Breakout
  <https://www.adafruit.com/product/2471>`_ (Product ID: 2471)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import gc
import time
from digitalio import Direction

__version__ = "0.5.6"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_espATcontrol.git"


class OKError(Exception):
    """The exception thrown when we didn't get acknowledgement to an AT command"""


class ESP_ATcontrol:
    """A wrapper for AT commands to a connected ESP8266 or ESP32 module to do
    some very basic internetting. The ESP module must be pre-programmed with
    AT command firmware, you can use esptool or our CircuitPython miniesptool
    to upload firmware"""

    # pylint: disable=too-many-public-methods, too-many-instance-attributes
    MODE_STATION = 1
    MODE_SOFTAP = 2
    MODE_SOFTAPSTATION = 3
    TYPE_TCP = "TCP"
    TCP_MODE = "TCP"
    TYPE_UDP = "UDP"
    TYPE_SSL = "SSL"
    TLS_MODE = "SSL"
    STATUS_APCONNECTED = 2
    STATUS_SOCKETOPEN = 3
    STATUS_SOCKETCLOSED = 4
    STATUS_NOTCONNECTED = 5
    USER_AGENT = "esp-idf/1.0 esp32"

    def __init__(
        self,
        uart,
        default_baudrate,
        *,
        run_baudrate=None,
        rts_pin=None,
        reset_pin=None,
        debug=False
    ):
        """This function doesn't try to do any sync'ing, just sets up
        # the hardware, that way nothing can unexpectedly fail!"""
        self._uart = uart
        if not run_baudrate:
            run_baudrate = default_baudrate
        self._default_baudrate = default_baudrate
        self._run_baudrate = run_baudrate
        self._uart.baudrate = default_baudrate

        self._reset_pin = reset_pin
        self._rts_pin = rts_pin
        if self._reset_pin:
            self._reset_pin.direction = Direction.OUTPUT
            self._reset_pin.value = True
        if self._rts_pin:
            self._rts_pin.direction = Direction.OUTPUT
        self.hw_flow(True)

        self._debug = debug
        self._versionstrings = []
        self._version = None
        self._ipdpacket = bytearray(1500)
        self._ifconfig = []
        self._initialized = False

    def begin(self):
        """Initialize the module by syncing, resetting if necessary, setting up
        the desired baudrate, turning on single-socket mode, and configuring
        SSL support. Required before using the module but we dont do in __init__
        because this can throw an exception."""
        # Connect and sync
        for _ in range(3):
            try:
                if not self.sync() and not self.soft_reset():
                    self.hard_reset()
                    self.soft_reset()
                self.echo(False)
                # set flow control if required
                self.baudrate = self._run_baudrate
                # get and cache versionstring
                self.get_version()
                if self.cipmux != 0:
                    self.cipmux = 0
                try:
                    self.at_response("AT+CIPSSLSIZE=4096", retries=1, timeout=3)
                except OKError:
                    # ESP32 doesnt use CIPSSLSIZE, its ok!
                    self.at_response("AT+CIPSSLCCONF?")
                self._initialized = True
                return
            except OKError:
                pass  # retry

    def connect(self, secrets):
        """Repeatedly try to connect to an access point with the details in
        the passed in 'secrets' dictionary. Be sure 'ssid' and 'password' are
        defined in the secrets dict! If 'timezone' is set, we'll also configure
        SNTP"""
        # Connect to WiFi if not already
        retries = 3
        while True:
            try:
                if not self._initialized or retries == 0:
                    self.begin()
                retries = 3
                AP = self.remote_AP  # pylint: disable=invalid-name
                print("Connected to", AP[0])
                if AP[0] != secrets["ssid"]:
                    self.join_AP(secrets["ssid"], secrets["password"])
                    if "timezone" in secrets:
                        tzone = secrets["timezone"]
                        ntp = None
                        if "ntp_server" in secrets:
                            ntp = secrets["ntp_server"]
                        self.sntp_config(True, tzone, ntp)
                    print("My IP Address:", self.local_ip)
                return  # yay!
            except (RuntimeError, OKError) as exp:
                print("Failed to connect, retrying\n", exp)
                retries -= 1
                continue

    # *************************** SOCKET SETUP ****************************

    @property
    def cipmux(self):
        """The IP socket multiplexing setting. 0 for one socket, 1 for multi-socket"""
        replies = self.at_response("AT+CIPMUX?", timeout=3).split(b"\r\n")
        for reply in replies:
            if reply.startswith(b"+CIPMUX:"):
                return int(reply[8:])
        raise RuntimeError("Bad response to CIPMUX?")

    def socket_connect(self, conntype, remote, remote_port, *, keepalive=10, retries=1):
        """Open a socket. conntype can be TYPE_TCP, TYPE_UDP, or TYPE_SSL. Remote
        can be an IP address or DNS (we'll do the lookup for you. Remote port
        is integer port on other side. We can't set the local port"""
        # lets just do one connection at a time for now
        while True:
            stat = self.status
            if stat in (self.STATUS_APCONNECTED, self.STATUS_SOCKETCLOSED):
                break
            if stat == self.STATUS_SOCKETOPEN:
                self.socket_disconnect()
            else:
                time.sleep(1)
        if not conntype in (self.TYPE_TCP, self.TYPE_UDP, self.TYPE_SSL):
            raise RuntimeError("Connection type must be TCP, UDL or SSL")
        cmd = (
            'AT+CIPSTART="'
            + conntype
            + '","'
            + remote
            + '",'
            + str(remote_port)
            + ","
            + str(keepalive)
        )
        replies = self.at_response(cmd, timeout=10, retries=retries).split(b"\r\n")
        for reply in replies:
            if reply == b"CONNECT" and self.status == self.STATUS_SOCKETOPEN:
                return True
        return False

    def socket_send(self, buffer, timeout=1):
        """Send data over the already-opened socket, buffer must be bytes"""
        cmd = "AT+CIPSEND=%d" % len(buffer)
        self.at_response(cmd, timeout=5, retries=1)
        prompt = b""
        stamp = time.monotonic()
        while (time.monotonic() - stamp) < timeout:
            if self._uart.in_waiting:
                prompt += self._uart.read(1)
                self.hw_flow(False)
                # print(prompt)
                if prompt[-1:] == b">":
                    break
            else:
                self.hw_flow(True)
        if not prompt or (prompt[-1:] != b">"):
            raise RuntimeError("Didn't get data prompt for sending")
        self._uart.reset_input_buffer()
        self._uart.write(buffer)
        stamp = time.monotonic()
        response = b""
        while (time.monotonic() - stamp) < timeout:
            if self._uart.in_waiting:
                response += self._uart.read(self._uart.in_waiting)
                if response[-9:] == b"SEND OK\r\n":
                    break
                if response[-7:] == b"ERROR\r\n":
                    break
        if self._debug:
            print("<---", response)
        # Get newlines off front and back, then split into lines
        return True

    def socket_receive(self, timeout=5):
        # pylint: disable=too-many-nested-blocks, too-many-branches
        """Check for incoming data over the open socket, returns bytes"""
        incoming_bytes = None
        bundle = []
        toread = 0
        gc.collect()
        i = 0  # index into our internal packet
        stamp = time.monotonic()
        ipd_start = b"+IPD,"
        while (time.monotonic() - stamp) < timeout:
            if self._uart.in_waiting:
                stamp = time.monotonic()  # reset timestamp when there's data!
                if not incoming_bytes:
                    self.hw_flow(False)  # stop the flow
                    # read one byte at a time
                    self._ipdpacket[i] = self._uart.read(1)[0]
                    if chr(self._ipdpacket[0]) != "+":
                        i = 0  # keep goin' till we start with +
                        continue
                    i += 1
                    # look for the IPD message
                    if (ipd_start in self._ipdpacket) and chr(
                        self._ipdpacket[i - 1]
                    ) == ":":
                        try:
                            ipd = str(self._ipdpacket[5 : i - 1], "utf-8")
                            incoming_bytes = int(ipd)
                            if self._debug:
                                print("Receiving:", incoming_bytes)
                        except ValueError as err:
                            raise RuntimeError(
                                "Parsing error during receive", ipd
                            ) from err
                        i = 0  # reset the input buffer now that we know the size
                    elif i > 20:
                        i = 0  # Hmm we somehow didnt get a proper +IPD packet? start over

                else:
                    self.hw_flow(False)  # stop the flow
                    # read as much as we can!
                    toread = min(incoming_bytes - i, self._uart.in_waiting)
                    # print("i ", i, "to read:", toread)
                    self._ipdpacket[i : i + toread] = self._uart.read(toread)
                    i += toread
                    if i == incoming_bytes:
                        # print(self._ipdpacket[0:i])
                        gc.collect()
                        bundle.append(self._ipdpacket[0:i])
                        gc.collect()
                        i = incoming_bytes = 0
                        break  # We've received all the data. Don't wait until timeout.
            else:  # no data waiting
                self.hw_flow(True)  # start the floooow
        totalsize = sum([len(x) for x in bundle])
        ret = bytearray(totalsize)
        i = 0
        for x in bundle:
            for char in x:
                ret[i] = char
                i += 1
        for x in bundle:
            del x
        gc.collect()
        return ret

    def socket_disconnect(self):
        """Close any open socket, if there is one"""
        try:
            self.at_response("AT+CIPCLOSE", retries=1)
        except OKError:
            pass  # this is ok, means we didn't have an open socket

    # *************************** SNTP SETUP ****************************

    def sntp_config(self, enable, timezone=None, server=None):
        """Configure the built in ESP SNTP client with a UTC-offset number (timezone)
        and server as IP or hostname."""
        cmd = "AT+CIPSNTPCFG="
        if enable:
            cmd += "1"
        else:
            cmd += "0"
        if timezone is not None:
            cmd += ",%d" % timezone
        if server is not None:
            cmd += ',"%s"' % server
        self.at_response(cmd, timeout=3)

    @property
    def sntp_time(self):
        """Return a string with time/date information using SNTP, may return
        1970 'bad data' on the first few minutes, without warning!"""
        replies = self.at_response("AT+CIPSNTPTIME?", timeout=5).split(b"\r\n")
        for reply in replies:
            if reply.startswith(b"+CIPSNTPTIME:"):
                return reply[13:]
        return None

    # *************************** WIFI SETUP ****************************

    @property
    def is_connected(self):
        """Initialize module if not done yet, and check if we're connected to
        an access point, returns True or False"""
        if not self._initialized:
            self.begin()
        try:
            self.echo(False)
            self.baudrate = self.baudrate
            stat = self.status
            if stat in (
                self.STATUS_APCONNECTED,
                self.STATUS_SOCKETOPEN,
                self.STATUS_SOCKETCLOSED,
            ):
                return True
        except (OKError, RuntimeError):
            pass
        return False

    @property
    def status(self):
        """The IP connection status number (see AT+CIPSTATUS datasheet for meaning)"""
        replies = self.at_response("AT+CIPSTATUS", timeout=5).split(b"\r\n")
        for reply in replies:
            if reply.startswith(b"STATUS:"):
                return int(reply[7:8])
        return None

    @property
    def mode(self):
        """What mode we're in, can be MODE_STATION, MODE_SOFTAP or MODE_SOFTAPSTATION"""
        if not self._initialized:
            self.begin()
        replies = self.at_response("AT+CWMODE?", timeout=5).split(b"\r\n")
        for reply in replies:
            if reply.startswith(b"+CWMODE:"):
                return int(reply[8:])
        raise RuntimeError("Bad response to CWMODE?")

    @mode.setter
    def mode(self, mode):
        """Station or AP mode selection, can be MODE_STATION, MODE_SOFTAP or MODE_SOFTAPSTATION"""
        if not self._initialized:
            self.begin()
        if not mode in (1, 2, 3):
            raise RuntimeError("Invalid Mode")
        self.at_response("AT+CWMODE=%d" % mode, timeout=3)

    @property
    def local_ip(self):
        """Our local IP address as a dotted-quad string"""
        reply = self.at_response("AT+CIFSR").strip(b"\r\n")
        for line in reply.split(b"\r\n"):
            if line and line.startswith(b'+CIFSR:STAIP,"'):
                return str(line[14:-1], "utf-8")
        raise RuntimeError("Couldn't find IP address")

    def ping(self, host):
        """Ping the IP or hostname given, returns ms time or None on failure"""
        reply = self.at_response('AT+PING="%s"' % host.strip('"'), timeout=5)
        for line in reply.split(b"\r\n"):
            if line and line.startswith(b"+"):
                try:
                    if line[1:5] == b"PING":
                        return int(line[6:])
                    return int(line[1:])
                except ValueError:
                    return None
        raise RuntimeError("Couldn't ping")

    def nslookup(self, host):
        """Return a dotted-quad IP address strings that matches the hostname"""
        reply = self.at_response('AT+CIPDOMAIN="%s"' % host.strip('"'), timeout=3)
        for line in reply.split(b"\r\n"):
            if line and line.startswith(b"+CIPDOMAIN:"):
                return str(line[11:], "utf-8").strip('"')
        raise RuntimeError("Couldn't find IP address")

    # *************************** AP SETUP ****************************

    @property
    def remote_AP(self):  # pylint: disable=invalid-name
        """The name of the access point we're connected to, as a string"""
        stat = self.status
        if stat != self.STATUS_APCONNECTED:
            return [None] * 4
        replies = self.at_response("AT+CWJAP?", timeout=10).split(b"\r\n")
        for reply in replies:
            if not reply.startswith("+CWJAP:"):
                continue
            reply = reply[7:].split(b",")
            for i, val in enumerate(reply):
                reply[i] = str(val, "utf-8")
                try:
                    reply[i] = int(reply[i])
                except ValueError:
                    reply[i] = reply[i].strip('"')  # its a string!
            return reply
        return [None] * 4

    def join_AP(self, ssid, password):  # pylint: disable=invalid-name
        """Try to join an access point by name and password, will return
        immediately if we're already connected and won't try to reconnect"""
        # First make sure we're in 'station' mode so we can connect to AP's
        if self.mode != self.MODE_STATION:
            self.mode = self.MODE_STATION

        router = self.remote_AP
        if router and router[0] == ssid:
            return  # we're already connected!
        for _ in range(3):
            reply = self.at_response(
                'AT+CWJAP="' + ssid + '","' + password + '"', timeout=15, retries=3
            )
            if b"WIFI CONNECTED" not in reply:
                print("no CONNECTED")
                raise RuntimeError("Couldn't connect to WiFi")
            if b"WIFI GOT IP" not in reply:
                print("no IP")
                raise RuntimeError("Didn't get IP address")
            return

    def scan_APs(self, retries=3):  # pylint: disable=invalid-name
        """Ask the module to scan for access points and return a list of lists
        with name, RSSI, MAC addresses, etc"""
        for _ in range(retries):
            try:
                if self.mode != self.MODE_STATION:
                    self.mode = self.MODE_STATION
                scan = self.at_response("AT+CWLAP", timeout=5).split(b"\r\n")
            except RuntimeError:
                continue
            routers = []
            for line in scan:
                if line.startswith(b"+CWLAP:("):
                    router = line[8:-1].split(b",")
                    for i, val in enumerate(router):
                        router[i] = str(val, "utf-8")
                        try:
                            router[i] = int(router[i])
                        except ValueError:
                            router[i] = router[i].strip('"')  # its a string!
                    routers.append(router)
            return routers

    # ************************** AT LOW LEVEL ****************************

    @property
    def version(self):
        """The cached version string retrieved via the AT+GMR command"""
        return self._version

    def get_version(self):
        """Request the AT firmware version string and parse out the
        version number"""
        reply = self.at_response("AT+GMR", timeout=3).strip(b"\r\n")
        self._version = None
        for line in reply.split(b"\r\n"):
            if line:
                self._versionstrings.append(str(line, "utf-8"))
                # get the actual version out
                if b"AT version:" in line:
                    self._version = str(line, "utf-8")
        return self._version

    def hw_flow(self, flag):
        """Turn on HW flow control (if available) on to allow data, or off to stop"""
        if self._rts_pin:
            self._rts_pin.value = not flag

    def at_response(self, at_cmd, timeout=5, retries=3):
        """Send an AT command, check that we got an OK response,
        and then cut out the reply lines to return. We can set
        a variable timeout (how long we'll wait for response) and
        how many times to retry before giving up"""
        # pylint: disable=too-many-branches
        for _ in range(retries):
            self.hw_flow(True)  # allow any remaning data to stream in
            time.sleep(0.1)  # wait for uart data
            self._uart.reset_input_buffer()  # flush it
            self.hw_flow(False)  # and shut off flow control again
            if self._debug:
                print("--->", at_cmd)
            self._uart.write(bytes(at_cmd, "utf-8"))
            self._uart.write(b"\x0d\x0a")
            stamp = time.monotonic()
            response = b""
            while (time.monotonic() - stamp) < timeout:
                if self._uart.in_waiting:
                    response += self._uart.read(1)
                    self.hw_flow(False)
                    if response[-4:] == b"OK\r\n":
                        break
                    if response[-7:] == b"ERROR\r\n":
                        break
                    if "AT+CWJAP=" in at_cmd:
                        if b"WIFI GOT IP\r\n" in response:
                            break
                    else:
                        if b"WIFI CONNECTED\r\n" in response:
                            break
                    if b"ERR CODE:" in response:
                        break
                else:
                    self.hw_flow(True)
            # eat beginning \n and \r
            if self._debug:
                print("<---", response)
            # special case, AT+CWJAP= does not return an ok :P
            if "AT+CWJAP=" in at_cmd and b"WIFI GOT IP\r\n" in response:
                return response
            # special case, ping also does not return an OK
            if "AT+PING" in at_cmd and b"ERROR\r\n" in response:
                return response
            if response[-4:] != b"OK\r\n":
                time.sleep(1)
                continue
            return response[:-4]
        raise OKError("No OK response to " + at_cmd)

    def sync(self):
        """Check if we have AT commmand sync by sending plain ATs"""
        try:
            self.at_response("AT", timeout=1)
            return True
        except OKError:
            return False

    @property
    def baudrate(self):
        """The baudrate of our UART connection"""
        return self._uart.baudrate

    @baudrate.setter
    def baudrate(self, baudrate):
        """Change the modules baudrate via AT commands and then check
        that we're still sync'd."""
        at_cmd = "AT+UART_CUR=" + str(baudrate) + ",8,1,0,"
        if self._rts_pin is not None:
            at_cmd += "2"
        else:
            at_cmd += "0"
        at_cmd += "\r\n"
        if self._debug:
            print("Changing baudrate to:", baudrate)
            print("--->", at_cmd)
        self._uart.write(bytes(at_cmd, "utf-8"))
        time.sleep(0.25)
        self._uart.baudrate = baudrate
        time.sleep(0.25)
        self._uart.reset_input_buffer()
        if not self.sync():
            raise RuntimeError("Failed to resync after Baudrate change")

    def echo(self, echo):
        """Set AT command echo on or off"""
        if echo:
            self.at_response("ATE1", timeout=1)
        else:
            self.at_response("ATE0", timeout=1)

    def soft_reset(self):
        """Perform a software reset by AT command. Returns True
        if we successfully performed, false if failed to reset"""
        try:
            self._uart.reset_input_buffer()
            reply = self.at_response("AT+RST", timeout=1)
            if reply.strip(b"\r\n") == b"AT+RST":
                time.sleep(2)
                self._uart.reset_input_buffer()
                return True
        except OKError:
            pass  # fail, see below
        return False

    def factory_reset(self):
        """Perform a hard reset, then send factory restore settings request"""
        self.hard_reset()
        self.at_response("AT+RESTORE", timeout=1)
        self._initialized = False

    def hard_reset(self):
        """Perform a hardware reset by toggling the reset pin, if it was
        defined in the initialization of this object"""
        if self._reset_pin:
            self._reset_pin.direction = Direction.OUTPUT
            self._reset_pin.value = False
            time.sleep(0.1)
            self._reset_pin.value = True
            self._uart.baudrate = self._default_baudrate
            time.sleep(3)  # give it a few seconds to wake up
            self._uart.reset_input_buffer()
            self._initialized = False
