# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2020 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_requests`
================================================================================

A requests-like library for web interfacing


* Author(s): ladyada, Paul Sokolovsky, Scott Shawcroft

Implementation Notes
--------------------

Adapted from https://github.com/micropython/micropython-lib/tree/master/urequests

micropython-lib consists of multiple modules from different sources and
authors. Each module comes under its own licensing terms. Short name of
a license can be found in a file within a module directory (usually
metadata.txt or setup.py). Complete text of each license used is provided
at https://github.com/micropython/micropython-lib/blob/master/LICENSE

author='Paul Sokolovsky'
license='MIT'

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

__version__ = "1.10.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Requests.git"

import errno

# CircuitPython 6.0 does not have the bytearray.split method.
# This function emulates buf.split(needle)[0], which is the functionality
# required.
def _buffer_split0(buf, needle):
    index = buf.find(needle)
    if index == -1:
        return buf
    return buf[:index]


class _RawResponse:
    def __init__(self, response):
        self._response = response

    def read(self, size=-1):
        """Read as much as available or up to size and return it in a byte string.

        Do NOT use this unless you really need to. Reusing memory with `readinto` is much better.
        """
        if size == -1:
            return self._response.content
        return self._response.socket.recv(size)

    def readinto(self, buf):
        """Read as much as available into buf or until it is full. Returns the number of bytes read
        into buf."""
        return self._response._readinto(buf)  # pylint: disable=protected-access


class _SendFailed(Exception):
    """Custom exception to abort sending a request."""


class OutOfRetries(Exception):
    """Raised when requests has retried to make a request unsuccessfully."""


class Response:
    """The response from a request, contains all the headers/content"""

    # pylint: disable=too-many-instance-attributes

    encoding = None

    def __init__(self, sock, session=None):
        self.socket = sock
        self.encoding = "utf-8"
        self._cached = None
        self._headers = {}

        # _start_index and _receive_buffer are used when parsing headers.
        # _receive_buffer will grow by 32 bytes everytime it is too small.
        self._received_length = 0
        self._receive_buffer = bytearray(32)
        self._remaining = None
        self._chunked = False

        self._backwards_compatible = not hasattr(sock, "recv_into")

        http = self._readto(b" ")
        if not http:
            if session:
                session._close_socket(self.socket)
            else:
                self.socket.close()
            raise RuntimeError("Unable to read HTTP response.")
        self.status_code = int(bytes(self._readto(b" ")))
        self.reason = self._readto(b"\r\n")
        self._parse_headers()
        self._raw = None
        self._session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _recv_into(self, buf, size=0):
        if self._backwards_compatible:
            size = len(buf) if size == 0 else size
            b = self.socket.recv(size)
            read_size = len(b)
            buf[:read_size] = b
            return read_size
        return self.socket.recv_into(buf, size)

    @staticmethod
    def _find(buf, needle, start, end):
        if hasattr(buf, "find"):
            return buf.find(needle, start, end)
        result = -1
        i = start
        while i < end:
            j = 0
            while j < len(needle) and i + j < end and buf[i + j] == needle[j]:
                j += 1
            if j == len(needle):
                result = i
                break
            i += 1

        return result

    def _readto(self, first, second=b""):
        buf = self._receive_buffer
        end = self._received_length
        while True:
            firsti = self._find(buf, first, 0, end)
            secondi = -1
            if second:
                secondi = self._find(buf, second, 0, end)

            i = -1
            needle_len = 0
            if firsti >= 0:
                i = firsti
                needle_len = len(first)
            if secondi >= 0 and (firsti < 0 or secondi < firsti):
                i = secondi
                needle_len = len(second)
            if i >= 0:
                result = buf[:i]
                new_start = i + needle_len

                if i + needle_len <= end:
                    new_end = end - new_start
                    buf[:new_end] = buf[new_start:end]
                    self._received_length = new_end
                return result

            # Not found so load more.

            # If our buffer is full, then make it bigger to load more.
            if end == len(buf):
                new_size = len(buf) + 32
                new_buf = bytearray(new_size)
                new_buf[: len(buf)] = buf
                buf = new_buf
                self._receive_buffer = buf

            read = self._recv_into(memoryview(buf)[end:])
            if read == 0:
                self._received_length = 0
                return buf[:end]
            end += read

        return b""

    def _read_from_buffer(self, buf=None, nbytes=None):
        if self._received_length == 0:
            return 0
        read = self._received_length
        if nbytes < read:
            read = nbytes
        membuf = memoryview(self._receive_buffer)
        if buf:
            buf[:read] = membuf[:read]
        if read < self._received_length:
            new_end = self._received_length - read
            self._receive_buffer[:new_end] = membuf[read : self._received_length]
            self._received_length = new_end
        else:
            self._received_length = 0
        return read

    def _readinto(self, buf):
        if not self.socket:
            raise RuntimeError(
                "Newer Response closed this one. Use Responses immediately."
            )

        if not self._remaining:
            # Consume the chunk header if need be.
            if self._chunked:
                # Consume trailing \r\n for chunks 2+
                if self._remaining == 0:
                    self._throw_away(2)
                chunk_header = _buffer_split0(self._readto(b"\r\n"), b";")
                http_chunk_size = int(bytes(chunk_header), 16)
                if http_chunk_size == 0:
                    self._chunked = False
                    self._parse_headers()
                    return 0
                self._remaining = http_chunk_size
            else:
                return 0

        nbytes = len(buf)
        if nbytes > self._remaining:
            nbytes = self._remaining

        read = self._read_from_buffer(buf, nbytes)
        if read == 0:
            read = self._recv_into(buf, nbytes)
        self._remaining -= read

        return read

    def _throw_away(self, nbytes):
        nbytes -= self._read_from_buffer(nbytes=nbytes)

        buf = self._receive_buffer
        for _ in range(nbytes // len(buf)):
            self._recv_into(buf)
        remaining = nbytes % len(buf)
        if remaining:
            self._recv_into(buf, remaining)

    def close(self):
        """Drain the remaining ESP socket buffers. We assume we already got what we wanted."""
        if not self.socket:
            return
        # Make sure we've read all of our response.
        if self._cached is None:
            if self._remaining and self._remaining > 0:
                self._throw_away(self._remaining)
            elif self._chunked:
                while True:
                    chunk_header = _buffer_split0(self._readto(b"\r\n"), b";")
                    chunk_size = int(bytes(chunk_header), 16)
                    if chunk_size == 0:
                        break
                    self._throw_away(chunk_size + 2)
                self._parse_headers()
        if self._session:
            self._session._free_socket(self.socket)  # pylint: disable=protected-access
        else:
            self.socket.close()
        self.socket = None

    def _parse_headers(self):
        """
        Parses the header portion of an HTTP request/response from the socket.
        Expects first line of HTTP request/response to have been read already.
        """
        while True:
            title = self._readto(b": ", b"\r\n")
            if not title:
                break

            content = self._readto(b"\r\n")
            if title and content:
                # enforce that all headers are lowercase
                title = str(title, "utf-8").lower()
                content = str(content, "utf-8")
                if title == "content-length":
                    self._remaining = int(content)
                if title == "transfer-encoding":
                    self._chunked = content.strip().lower() == "chunked"
                self._headers[title] = content

    @property
    def headers(self):
        """
        The response headers. Does not include headers from the trailer until
        the content has been read.
        """
        return self._headers

    @property
    def content(self):
        """The HTTP content direct from the socket, as bytes"""
        if self._cached is not None:
            if isinstance(self._cached, bytes):
                return self._cached
            raise RuntimeError("Cannot access content after getting text or json")

        self._cached = b"".join(self.iter_content(chunk_size=32))
        return self._cached

    @property
    def text(self):
        """The HTTP content, encoded into a string according to the HTTP
        header encoding"""
        if self._cached is not None:
            if isinstance(self._cached, str):
                return self._cached
            raise RuntimeError("Cannot access text after getting content or json")
        self._cached = str(self.content, self.encoding)
        return self._cached

    def json(self):
        """The HTTP content, parsed into a json dictionary"""
        # pylint: disable=import-outside-toplevel
        import json

        # The cached JSON will be a list or dictionary.
        if self._cached:
            if isinstance(self._cached, (list, dict)):
                return self._cached
            raise RuntimeError("Cannot access json after getting text or content")
        if not self._raw:
            self._raw = _RawResponse(self)

        try:
            obj = json.load(self._raw)
        except OSError:
            # <5.3.1 doesn't piecemeal load json from any object with readinto so load the whole
            # string.
            obj = json.loads(self._raw.read())
        if not self._cached:
            self._cached = obj
        self.close()
        return obj

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """An iterator that will stream data by only reading 'chunk_size'
        bytes and yielding them, when we can't buffer the whole datastream"""
        if decode_unicode:
            raise NotImplementedError("Unicode not supported")

        b = bytearray(chunk_size)
        while True:
            size = self._readinto(b)
            if size == 0:
                break
            if size < chunk_size:
                chunk = bytes(memoryview(b)[:size])
            else:
                chunk = bytes(b)
            yield chunk
        self.close()


class Session:
    """HTTP session that shares sockets and ssl context."""

    def __init__(self, socket_pool, ssl_context=None):
        self._socket_pool = socket_pool
        self._ssl_context = ssl_context
        # Hang onto open sockets so that we can reuse them.
        self._open_sockets = {}
        self._socket_free = {}
        self._last_response = None

    def _free_socket(self, socket):
        if socket not in self._open_sockets.values():
            raise RuntimeError("Socket not from session")
        self._socket_free[socket] = True

    def _close_socket(self, sock):
        sock.close()
        del self._socket_free[sock]
        key = None
        for k in self._open_sockets:
            if self._open_sockets[k] == sock:
                key = k
                break
        if key:
            del self._open_sockets[key]

    def _free_sockets(self):
        free_sockets = []
        for sock in self._socket_free:
            if self._socket_free[sock]:
                free_sockets.append(sock)
        for sock in free_sockets:
            self._close_socket(sock)

    def _get_socket(self, host, port, proto, *, timeout=1):
        # pylint: disable=too-many-branches
        key = (host, port, proto)
        if key in self._open_sockets:
            sock = self._open_sockets[key]
            if self._socket_free[sock]:
                self._socket_free[sock] = False
                return sock
        if proto == "https:" and not self._ssl_context:
            raise RuntimeError(
                "ssl_context must be set before using adafruit_requests for https"
            )
        addr_info = self._socket_pool.getaddrinfo(
            host, port, 0, self._socket_pool.SOCK_STREAM
        )[0]
        retry_count = 0
        sock = None
        while retry_count < 5 and sock is None:
            if retry_count > 0:
                if any(self._socket_free.items()):
                    self._free_sockets()
                else:
                    raise RuntimeError("Sending request failed")
            retry_count += 1

            try:
                sock = self._socket_pool.socket(
                    addr_info[0], addr_info[1], addr_info[2]
                )
            except OSError:
                continue
            except RuntimeError:
                continue

            connect_host = addr_info[-1][0]
            if proto == "https:":
                sock = self._ssl_context.wrap_socket(sock, server_hostname=host)
                connect_host = host
            sock.settimeout(timeout)  # socket read timeout

            try:
                sock.connect((connect_host, port))
            except MemoryError:
                sock.close()
                sock = None
            except OSError:
                sock.close()
                sock = None

        if sock is None:
            raise RuntimeError("Repeated socket failures")

        self._open_sockets[key] = sock
        self._socket_free[sock] = False
        return sock

    @staticmethod
    def _send(socket, data):
        total_sent = 0
        while total_sent < len(data):
            # ESP32SPI sockets raise a RuntimeError when unable to send.
            try:
                sent = socket.send(data[total_sent:])
            except RuntimeError:
                sent = 0
            if sent is None:
                sent = len(data)
            if sent == 0:
                raise _SendFailed()
            total_sent += sent

    def _send_request(self, socket, host, method, path, headers, data, json):
        # pylint: disable=too-many-arguments
        self._send(socket, bytes(method, "utf-8"))
        self._send(socket, b" /")
        self._send(socket, bytes(path, "utf-8"))
        self._send(socket, b" HTTP/1.1\r\n")
        if "Host" not in headers:
            self._send(socket, b"Host: ")
            self._send(socket, bytes(host, "utf-8"))
            self._send(socket, b"\r\n")
        if "User-Agent" not in headers:
            self._send(socket, b"User-Agent: Adafruit CircuitPython\r\n")
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            self._send(socket, k.encode())
            self._send(socket, b": ")
            self._send(socket, headers[k].encode())
            self._send(socket, b"\r\n")
        if json is not None:
            assert data is None
            # pylint: disable=import-outside-toplevel
            try:
                import json as json_module
            except ImportError:
                import ujson as json_module
            data = json_module.dumps(json)
            self._send(socket, b"Content-Type: application/json\r\n")
        if data:
            if isinstance(data, dict):
                self._send(
                    socket, b"Content-Type: application/x-www-form-urlencoded\r\n"
                )
                _post_data = ""
                for k in data:
                    _post_data = "{}&{}={}".format(_post_data, k, data[k])
                data = _post_data[1:]
            self._send(socket, b"Content-Length: %d\r\n" % len(data))
        self._send(socket, b"\r\n")
        if data:
            if isinstance(data, bytearray):
                self._send(socket, bytes(data))
            else:
                self._send(socket, bytes(data, "utf-8"))

    # pylint: disable=too-many-branches, too-many-statements, unused-argument, too-many-arguments, too-many-locals
    def request(
        self, method, url, data=None, json=None, headers=None, stream=False, timeout=60
    ):
        """Perform an HTTP request to the given url which we will parse to determine
        whether to use SSL ('https://') or not. We can also send some provided 'data'
        or a json dictionary which we will stringify. 'headers' is optional HTTP headers
        sent along. 'stream' will determine if we buffer everything, or whether to only
        read only when requested
        """
        if not headers:
            headers = {}

        try:
            proto, dummy, host, path = url.split("/", 3)
            # replace spaces in path
            path = path.replace(" ", "%20")
        except ValueError:
            proto, dummy, host = url.split("/", 2)
            path = ""
        if proto == "http:":
            port = 80
        elif proto == "https:":
            port = 443
        else:
            raise ValueError("Unsupported protocol: " + proto)

        if ":" in host:
            host, port = host.split(":", 1)
            port = int(port)

        if self._last_response:
            self._last_response.close()
            self._last_response = None

        # We may fail to send the request if the socket we got is closed already. So, try a second
        # time in that case.
        retry_count = 0
        while retry_count < 2:
            retry_count += 1
            socket = self._get_socket(host, port, proto, timeout=timeout)
            ok = True
            try:
                self._send_request(socket, host, method, path, headers, data, json)
            except (_SendFailed, OSError):
                ok = False
            if ok:
                # Read the H of "HTTP/1.1" to make sure the socket is alive. send can appear to work
                # even when the socket is closed.
                if hasattr(socket, "recv"):
                    result = socket.recv(1)
                else:
                    result = bytearray(1)
                    try:
                        socket.recv_into(result)
                    except OSError:
                        pass
                if result == b"H":
                    # Things seem to be ok so break with socket set.
                    break
            self._close_socket(socket)
            socket = None

        if not socket:
            raise OutOfRetries("Repeated socket failures")

        resp = Response(socket, self)  # our response
        if "location" in resp.headers and 300 <= resp.status_code <= 399:
            # a naive handler for redirects
            redirect = resp.headers["location"]

            if redirect.startswith("http"):
                # absolute URL
                url = redirect
            elif redirect[0] == "/":
                # relative URL, absolute path
                url = "/".join([proto, dummy, host, redirect[1:]])
            else:
                # relative URL, relative path
                path = path.rsplit("/", 1)[0]

                while redirect.startswith("../"):
                    path = path.rsplit("/", 1)[0]
                    redirect = redirect.split("../", 1)[1]

                url = "/".join([proto, dummy, host, path, redirect])

            self._last_response = resp
            resp = self.request(method, url, data, json, headers, stream, timeout)

        self._last_response = resp
        return resp

    def head(self, url, **kw):
        """Send HTTP HEAD request"""
        return self.request("HEAD", url, **kw)

    def get(self, url, **kw):
        """Send HTTP GET request"""
        return self.request("GET", url, **kw)

    def post(self, url, **kw):
        """Send HTTP POST request"""
        return self.request("POST", url, **kw)

    def put(self, url, **kw):
        """Send HTTP PUT request"""
        return self.request("PUT", url, **kw)

    def patch(self, url, **kw):
        """Send HTTP PATCH request"""
        return self.request("PATCH", url, **kw)

    def delete(self, url, **kw):
        """Send HTTP DELETE request"""
        return self.request("DELETE", url, **kw)


# Backwards compatible API:

_default_session = None  # pylint: disable=invalid-name


class _FakeSSLSocket:
    def __init__(self, socket, tls_mode):
        self._socket = socket
        self._mode = tls_mode
        self.settimeout = socket.settimeout
        self.send = socket.send
        self.recv = socket.recv
        self.close = socket.close

    def connect(self, address):
        """connect wrapper to add non-standard mode parameter"""
        try:
            return self._socket.connect(address, self._mode)
        except RuntimeError as error:
            raise OSError(errno.ENOMEM) from error


class _FakeSSLContext:
    def __init__(self, iface):
        self._iface = iface

    def wrap_socket(self, socket, server_hostname=None):
        """Return the same socket"""
        # pylint: disable=unused-argument
        return _FakeSSLSocket(socket, self._iface.TLS_MODE)


def set_socket(sock, iface=None):
    """Legacy API for setting the socket and network interface. Use a `Session` instead."""
    global _default_session  # pylint: disable=global-statement,invalid-name
    if not iface:
        # pylint: disable=protected-access
        _default_session = Session(sock, _FakeSSLContext(sock._the_interface))
    else:
        _default_session = Session(sock, _FakeSSLContext(iface))
    sock.set_interface(iface)


def request(method, url, data=None, json=None, headers=None, stream=False, timeout=1):
    """Send HTTP request"""
    # pylint: disable=too-many-arguments
    _default_session.request(
        method,
        url,
        data=data,
        json=json,
        headers=headers,
        stream=stream,
        timeout=timeout,
    )


def head(url, **kw):
    """Send HTTP HEAD request"""
    return _default_session.request("HEAD", url, **kw)


def get(url, **kw):
    """Send HTTP GET request"""
    return _default_session.request("GET", url, **kw)


def post(url, **kw):
    """Send HTTP POST request"""
    return _default_session.request("POST", url, **kw)


def put(url, **kw):
    """Send HTTP PUT request"""
    return _default_session.request("PUT", url, **kw)


def patch(url, **kw):
    """Send HTTP PATCH request"""
    return _default_session.request("PATCH", url, **kw)


def delete(url, **kw):
    """Send HTTP DELETE request"""
    return _default_session.request("DELETE", url, **kw)
