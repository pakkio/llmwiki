"""Fetch a user-supplied URL without letting the server reach private networks (SSRF).

Rules, applied to the URL and again to every redirect hop:
  * only http and https, no credentials in the URL;
  * the host must resolve only to public addresses (no loopback, private, link-local,
    CGNAT such as Tailscale, reserved or multicast ranges);
  * redirects are followed by hand, at most MAX_REDIRECTS times;
  * the body is capped at MAX_BYTES.

Known limit: the host is resolved once to check it and again by httpx to connect, so a
hostile DNS server that answers differently the second time (DNS rebinding) can still
slip through. Closing that needs connecting to the checked IP; with a login now
required it is a much smaller risk than the plain SSRF this module removes.
"""
import ipaddress
import socket
from urllib.parse import urljoin, urlsplit

import httpx

MAX_BYTES = 5 * 1024 * 1024
MAX_REDIRECTS = 5
TIMEOUT = 30


class UnsafeURL(ValueError):
    """The URL points somewhere the server must not fetch from."""


def _check_host(host: str, port: int) -> None:
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as e:
        raise UnsafeURL(f"cannot resolve host {host!r}") from e
    if not infos:
        raise UnsafeURL(f"cannot resolve host {host!r}")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
            ip = ip.ipv4_mapped
        if not ip.is_global:
            raise UnsafeURL(f"refusing to fetch from a non-public address (host {host!r})")


def _check_url(url: str) -> None:
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise UnsafeURL("only http and https URLs are allowed")
    if not parts.hostname:
        raise UnsafeURL("the URL has no host")
    if parts.username or parts.password:
        raise UnsafeURL("credentials in the URL are not allowed")
    try:
        port = parts.port or (443 if parts.scheme == "https" else 80)
    except ValueError as e:
        raise UnsafeURL("invalid port in the URL") from e
    _check_host(parts.hostname, port)


def fetch_public_text(url: str, *, transport: httpx.BaseTransport | None = None) -> str:
    """GET `url` and return its body as text; raise UnsafeURL or httpx errors."""
    current = url
    with httpx.Client(follow_redirects=False, timeout=TIMEOUT, transport=transport) as client:
        for _ in range(MAX_REDIRECTS + 1):
            _check_url(current)
            with client.stream("GET", current) as r:
                if r.is_redirect:
                    location = r.headers.get("location")
                    if not location:
                        raise UnsafeURL("redirect without a Location header")
                    current = urljoin(current, location)
                    continue
                r.raise_for_status()
                body = bytearray()
                for chunk in r.iter_bytes():
                    body += chunk
                    if len(body) > MAX_BYTES:
                        raise UnsafeURL(f"response larger than {MAX_BYTES} bytes")
                encoding = getattr(r, "charset_encoding", None) or "utf-8"
                return body.decode(encoding, errors="replace")
    raise UnsafeURL("too many redirects")
