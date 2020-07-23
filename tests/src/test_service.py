from src.service import handler


def test_is_callable():
    assert callable(handler)
