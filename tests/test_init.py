import zlib as zlib_original

import aiohttp.http_websocket

from aiohttp_zlib_ng import best_zlib, disable_zlib_ng, enable_zlib_ng


def test_enable_disable():
    """Test enable/disable."""
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_zlib_ng()
    assert aiohttp.http_websocket.zlib is best_zlib
    disable_zlib_ng()
    assert aiohttp.http_websocket.zlib is zlib_original
    enable_zlib_ng()
    assert aiohttp.http_websocket.zlib is best_zlib
    disable_zlib_ng()
