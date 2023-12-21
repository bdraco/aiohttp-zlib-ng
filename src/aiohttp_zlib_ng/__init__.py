__version__ = "0.0.0"

import importlib
import logging
import platform
import zlib as zlib_original
from typing import Any, Dict, Optional

import aiohttp
from zlib_ng import zlib_ng as zlib_ng

_LOGGER = logging.getLogger(__name__)

TARGETS = (
    "compression_utils",
    "http_writer",
    "http_websocket",
    "http_writer",
    "http_parser",
    "multipart",
    "web_response",
)

CPUFeature: Optional[Dict[str, Any]] = None

if platform.machine() == "x86_64":
    try:
        from cpufeature import CPUFeature  # type: ignore[no-redef]
    except ImportError:
        pass

HAS_MISSING_AVX = bool(CPUFeature and not CPUFeature.get("AVX"))
# HAS_MISSING_AVX is True if AVX is not supported and using x86_64.
#
# This is a workaround to disable zlib-ng on x86_64 if AVX is not supported
# on older CPUs until https://github.com/pycompression/python-zlib-ng/pull/15
# is merged and released.
#
# See https://github.com/home-assistant/core/issues/105254
#


def enable_zlib_ng() -> None:
    """Enable zlib-ng."""
    if HAS_MISSING_AVX:
        _LOGGER.debug("AVX is not supported, disabling zlib-ng")
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
    if HAS_MISSING_AVX:
        return
    for location in TARGETS:
        if module := getattr(aiohttp, location, None):
            module.zlib = zlib_original
