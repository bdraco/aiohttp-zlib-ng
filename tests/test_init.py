import zlib as zlib_original

import aiohttp.http_websocket
from zlib_ng import zlib_ng as zlib_ng

from aiohttp_zlib_ng import disable_zlib_ng, enable_zlib_ng


def test_enable_disable():
    """Test enable/disable."""
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_zlib_ng()
    assert aiohttp.http_websocket.zlib is zlib_ng
    disable_zlib_ng()
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_zlib_ng()
    assert aiohttp.http_websocket.zlib is zlib_ng
