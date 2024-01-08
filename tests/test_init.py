import zlib as zlib_original

import aiohttp.http_websocket

from aiohttp_zlib_ng import disable_zlib_ng, enable_zlib_ng

try:
    from isal import (  # type: ignore
        isal_zlib as expected_zlib,
    )
except ImportError:
    from zlib_ng import zlib_ng as expected_zlib


def test_enable_disable():
    """Test enable/disable."""
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_zlib_ng()
    assert aiohttp.http_websocket.zlib is expected_zlib
    disable_zlib_ng()
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_zlib_ng()
    assert aiohttp.http_websocket.zlib is expected_zlib
    disable_zlib_ng()
