# Author: Jiroawesome

import contextlib
import io
import os.path
import socket
import ssl
import sys
import urllib.parse
from http.client import HTTPConnection, HTTPSConnection, HTTPMessage, HTTPException

__version__ = "1.0.0"

__all__ = ["HTTPException", "TooManyRedirects", "Response",
           "yield_response", "request", "get", "post", "head", "put", "patch", "delete"]

DEFAULT_TIMEOUT = 15.0

DEFAULT_UA = "Python " + sys.version.split()[0]


def request(method, url, *, read_limit=None, **kwargs):
    with yield_response(method, url, **kwargs) as response:
        try:
            body = response.read(read_limit)
        except HTTPException:
            raise
        except IOError as e:
            raise HTTPException(str(e)) from e
        return Response(response.url, response.status, _prepare_incoming_headers(response.headers), body)


def get(url, **kwargs):
    return request("GET", url=url, **kwargs)


def post(url, body=None, **kwargs):
    return request("POST", url=url, body=body, **kwargs)


def head(url, **kwargs):
    return request("HEAD", url=url, **kwargs)


def put(url, body=None, **kwargs):
    return request("PUT", url=url, body=body, **kwargs)


def patch(url, body=None, **kwargs):
    return request("PATCH", url=url, body=body, **kwargs)


def delete(url, **kwargs):
    return request("DELETE", url=url, **kwargs)


@contextlib.contextmanager
def yield_response(method, url, *, unix_socket=None, timeout=DEFAULT_TIMEOUT, headers=None,
                   params=None, body=None, form=None, json=None, verify=True, source_address=None,
                   max_redirects=None, ssl_context=None):
    method = method.upper()
    headers = _prepare_outgoing_headers(headers)
    enc_params = _prepare_params(params)
    body = _prepare_body(body, form, json, headers)

    visited_urls = []

    while max_redirects is None or len(visited_urls) <= max_redirects:
        url, conn, path = _prepare_request(method, url, enc_params=enc_params, timeout=timeout, unix_socket=unix_socket, verify=verify, source_address=source_address, ssl_context=ssl_context)
        enc_params = ""
        visited_urls.append(url)
        try:
            try:
                conn.request(method, path, headers=headers, body=body)
                response = conn.getresponse()
            except HTTPException:
                raise
            except IOError as e:
                raise HTTPException(str(e)) from e
            redirect_url = _check_redirect(url, response.status, response.headers)
            if max_redirects is None or redirect_url is None:
                response.url = url
                yield response
                return
            else:
                url = redirect_url
                if response.status == 303:
                    method = "GET"
        finally:
            conn.close()

    raise TooManyRedirects(visited_urls)


class Response:
    __slots__ = ("url", "status_code", "headers", "body")

    def __init__(self, url, status_code, headers, body):
        self.url, self.status_code, self.headers, self.body = url, status_code, headers, body

    def __repr__(self):
        return f"Response(status_code={self.status_code:d})"

    @property
    def ok(self):
        return not (400 <= self.status_code < 600)

    @property
    def content(self):
        return self.body

    def raise_for_status(self):
        if not self.ok:
            raise HTTPErrorStatus(self.status_code)

    def json(self):
        import json as jsonlib
        return jsonlib.loads(self.body)

    def _debugstr(self):
        buf = io.StringIO()
        print("HTTP", self.status_code, file=buf)
        for k, v in self.headers.items():
            print(f"{k}: {v}", file=buf)
        print(file=buf)
        try:
            print(self.body.decode("utf-8"), file=buf)
        except UnicodeDecodeError:
            print(f"<{len(self.body)} bytes binary data>", file=buf)
        return buf.getvalue()


class TooManyRedirects(HTTPException):
    pass


class HTTPErrorStatus(HTTPException):
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return f"HTTP response returned error code {self.status_code:d}"


_JSON_CONTENTTYPE = "application/json"
_FORM_CONTENTTYPE = "application/x-www-form-urlencoded"


class UnixHTTPConnection(HTTPConnection):
    def __init__(self, path, timeout=DEFAULT_TIMEOUT):
        super(UnixHTTPConnection, self).__init__("localhost", timeout=timeout)
        self._unix_path = path

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.settimeout(self.timeout)
            sock.connect(self._unix_path)
        except Exception:
            sock.close()
            raise
        self.sock = sock


def _check_redirect(url, status, response_headers):
    if status not in (301, 302, 303, 307, 308):
        return None
    location = response_headers.get("Location")
    if not location:
        return None
    parsed_location = urllib.parse.urlparse(location)
    if parsed_location.scheme:
        return location

    old_url = urllib.parse.urlparse(url)
    if location.startswith("/"):
        return urllib.parse.urlunparse((old_url.scheme, old_url.netloc,
                                        parsed_location.path, parsed_location.params,
                                        parsed_location.query, parsed_location.fragment))

    old_dir, _old_file = os.path.split(old_url.path)
    new_path = os.path.join(old_dir, location)
    return urllib.parse.urlunparse((old_url.scheme, old_url.netloc,
                                    new_path, parsed_location.params,
                                    parsed_location.query, parsed_location.fragment))


def _prepare_outgoing_headers(headers):
    if headers is None:
        headers = HTTPMessage()
    elif not isinstance(headers, HTTPMessage):
        new_headers = HTTPMessage()
        if hasattr(headers, "items"):
            iterator = headers.items()
        else:
            iterator = iter(headers)
        for k, v in iterator:
            new_headers[k] = v
        headers = new_headers
    _setdefault_header(headers, "User-Agent", DEFAULT_UA)
    return headers


def _prepare_incoming_headers(headers):
    headers_dict = {}
    for k, v in headers.items():
        headers_dict.setdefault(k, []).append(v)
    result = HTTPMessage()
    for k, vlist in headers_dict.items():
        result[k] = ",".join(vlist)
    return result


def _setdefault_header(headers, name, value):
    if name not in headers:
        headers[name] = value


def _prepare_body(body, form, json, headers):
    if body is not None:
        if not isinstance(body, bytes):
            raise TypeError("[!] body must be bytes or None", type(body))
        return body

    if json is not None:
        _setdefault_header(headers, "Content-Type", _JSON_CONTENTTYPE)
        import json as jsonlib
        return jsonlib.dumps(json).encode("utf-8")

    if form is not None:
        _setdefault_header(headers, "Content-Type", _FORM_CONTENTTYPE)
        return urllib.parse.urlencode(form, doseq=True)

    return None


def _prepare_params(params):
    if params is None:
        return ""
    return urllib.parse.urlencode(params, doseq=True)


def _prepare_request(method, url, *, enc_params="", timeout=DEFAULT_TIMEOUT, source_address=None, unix_socket=None, verify=True, ssl_context=None):
    parsed_url = urllib.parse.urlparse(url)

    is_unix = (unix_socket is not None)
    scheme = parsed_url.scheme.lower()
    if scheme.endswith("+unix"):
        scheme = scheme[:-5]
        is_unix = True
        if scheme == "https":
            raise ValueError("[!] https+unix is not implemented")

    if scheme not in ("http", "https"):
        raise ValueError("[!] unrecognized scheme", scheme)

    is_https = (scheme == "https")
    host = parsed_url.hostname
    port = 443 if is_https else 80
    if parsed_url.port:
        port = parsed_url.port

    if is_unix and unix_socket is None:
        unix_socket = urllib.parse.unquote(parsed_url.netloc)

    path = parsed_url.path
    if parsed_url.query:
        if enc_params:
            path = f"{path}?{parsed_url.query}&{enc_params}"
        else:
            path = f"{path}?{parsed_url.query}"
    else:
        if enc_params:
            path = f"{path}?{enc_params}"
        else:
            pass

    if isinstance(source_address, str):
        source_address = (source_address, 0)

    if is_unix:
        conn = UnixHTTPConnection(unix_socket, timeout=timeout)
    elif is_https:
        if ssl_context is None:
            ssl_context = ssl.create_default_context()
            if not verify:
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
        conn = HTTPSConnection(host, port, source_address=source_address, timeout=timeout,
                               context=ssl_context)
    else:
        conn = HTTPConnection(host, port, source_address=source_address, timeout=timeout)

    simreqed_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc,
                                          path, parsed_url.params,
                                          "", parsed_url.fragment))
    return simreqed_url, conn, path