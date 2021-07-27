# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""A 'socket' compatible interface thru the ESP AT command set"""
from micropython import const

_the_interface = None  # pylint: disable=invalid-name


def set_interface(iface):
    """Helper to set the global internet interface"""
    global _the_interface  # pylint: disable=global-statement, invalid-name
    _the_interface = iface


SOCK_STREAM = const(1)
AF_INET = const(2)

# pylint: disable=too-many-arguments, unused-argument
def getaddrinfo(host, port, family=0, socktype=0, proto=0, flags=0):
    """Given a hostname and a port name, return a 'socket.getaddrinfo'
    compatible list of tuples. Honestly, we ignore anything but host & port"""
    if not isinstance(port, int):
        raise RuntimeError("port must be an integer")
    ipaddr = _the_interface.nslookup(host)
    return [(AF_INET, socktype, proto, "", (ipaddr, port))]


# pylint: enable=too-many-arguments, unused-argument


# pylint: disable=unused-argument, redefined-builtin, invalid-name
class socket:
    """A simplified implementation of the Python 'socket' class, for connecting
    through an interface to a remote device"""

    def __init__(self, family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None):
        if family != AF_INET:
            raise RuntimeError("Only AF_INET family supported")
        if type != SOCK_STREAM:
            raise RuntimeError("Only SOCK_STREAM type supported")
        self._buffer = b""
        self.settimeout(0)

    def connect(self, address, conntype=None):
        """Connect the socket to the 'address' (which should be dotted quad IP). 'conntype'
        is an extra that may indicate SSL or not, depending on the underlying interface"""
        host, port = address

        # Determine the conntype from port if not specified.
        if conntype is None:
            if port == 80:
                conntype = "TCP"
            elif port == 443:
                conntype = "SSL"

        if not _the_interface.socket_connect(
            conntype, host, port, keepalive=10, retries=3
        ):
            raise RuntimeError("Failed to connect to host", host)
        self._buffer = b""

    def send(self, data):  # pylint: disable=no-self-use
        """Send some data to the socket"""
        _the_interface.socket_send(data)

    def readline(self):
        """Attempt to return as many bytes as we can up to but not including '\r\n'"""
        if b"\r\n" not in self._buffer:
            # there's no line already in there, read some more
            self._buffer = self._buffer + _the_interface.socket_receive(timeout=3)
            # print(self._buffer)
        firstline, self._buffer = self._buffer.split(b"\r\n", 1)
        return firstline

    def recv(self, num=0):
        """Read up to 'num' bytes from the socket, this may be buffered internally!
        If 'num' isnt specified, return everything in the buffer."""
        if num == 0:
            # read as much as we can
            ret = self._buffer + _the_interface.socket_receive(timeout=self._timeout)
            self._buffer = b""
        else:
            if self._buffer == b"":
                self._buffer = self._buffer + _the_interface.socket_receive(
                    timeout=self._timeout
                )
            ret = self._buffer[:num]
            self._buffer = self._buffer[num:]
        return ret

    def close(self):
        """Close the socket, after reading whatever remains"""
        # read whatever's left
        self._buffer = self._buffer + _the_interface.socket_receive(
            timeout=self._timeout
        )
        _the_interface.socket_disconnect()

    def settimeout(self, value):
        """Set the read timeout for sockets, if value is 0 it will block"""
        self._timeout = value


# pylint: enable=unused-argument, redefined-builtin, invalid-name
