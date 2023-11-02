from aiohttp_zlib_ng.main import add


def test_add():
    assert add(1, 1) == 2
