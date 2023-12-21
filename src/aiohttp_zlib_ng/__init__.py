__version__ = "0.0.0"

import importlib
import platform
import zlib as zlib_original
from typing import Any

import aiohttp
from zlib_ng import zlib_ng as zlib_ng

TARGETS = (
    "compression_utils",
    "http_writer",
    "http_websocket",
    "http_writer",
    "http_parser",
    "multipart",
    "web_response",
)

CPUFeature: dict[str, Any] | None = None

try:
    from cpufeature import CPUFeature  # type: ignore[no-redef]
except ImportError:
    pass


def has_missing_avx_flag_on_x86_64() -> bool:
    """
    Return True if AVX is supported or not x86_64.

    This is a workaround to disable zlib-ng on x86_64 if AVX is not supported
    on older CPUs until https://github.com/pycompression/python-zlib-ng/pull/15
    is merged and released.

    See
    https://github.com/home-assistant/core/issues/105254
    """
    if platform.machine() != "x86_64":
        return False
    return bool(CPUFeature and not CPUFeature.get("AVX"))


def enable_zlib_ng() -> None:
    """Enable zlib-ng."""
    if has_missing_avx_flag_on_x86_64():
        return
    for location in TARGETS:
        try:
            importlib.import_module(f"aiohttp.{location}")
        except ImportError:
            continue
        if module := getattr(aiohttp, location, None):
            module.zlib = zlib_ng


def disable_zlib_ng() -> None:
    """Disable zlib-ng and restore the original zlib."""
    if has_missing_avx_flag_on_x86_64():
        return
    for location in TARGETS:
        if module := getattr(aiohttp, location, None):
            module.zlib = zlib_original
