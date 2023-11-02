__version__ = "0.0.0"

import importlib
import zlib as zlib_original

import aiohttp
from zlib_ng import zlib_ng as zlib_ng

TARGETS = (
    "compression_utils",
    "http_writer",
    "http_websocket",
    "http_writer",
    "multipart",
    "web_response",
)


def enable_zlib_ng() -> None:
    """Enable zlib-ng."""
    for location in TARGETS:
        try:
            importlib.import_module(f"aiohttp.{location}")
        except ImportError:
            continue
        if module := getattr(aiohttp, location, None):
            module.zlib = zlib_ng


def disable_zlib_ng() -> None:
    """Disable zlib-ng and restore the original zlib."""
    for location in TARGETS:
        if module := getattr(aiohttp, location, None):
            module.zlib = zlib_original
