import time
import pytest

from cdict import C

def assert_dicts(c, expected):
    print(c)
    dicts = list(c.dicts())
    assert len(dicts) == len(expected), f"Expected equal lengths, got {len(expected)} instead of {len(dicts)}"
    for i, (d1, d2) in enumerate(zip(dicts, expected)):
        assert d1 == d2, f"Mismatch at {i}, got {d1} instead of {d2}"


def test_simple():
    c1 = C.dict(a=5, b=3)
    assert_dicts(c1, [dict(a=5, b=3)])

    c2 = C.dict(nested=c1, c=4)
    assert_dicts(c2, [dict(nested=dict(a=5, b=3), c=4)])

    c3 = c1 + c2
    assert_dicts(c3, [
        dict(a=5, b=3),
        dict(nested=dict(a=5, b=3), c=4)
    ])

    c4 = c1 * c2
    assert_dicts(c4, [
        dict(a=5, b=3, nested=dict(a=5, b=3), c=4)
    ])

    c5 = c4 * c1
    assert_dicts(c5, [
        dict(a=5, b=3, nested=dict(a=5, b=3), c=4)
    ])

    c6 = C.dict(a=C.list(5, 6), b=3)
    assert_dicts(c6, [dict(a=5, b=3), dict(a=6, b=3)])

    c7 = C.dict(a=C.dict(a1=5, a2=6) + C.dict(a1=6, a2=5)) * C.dict(b=3)
    assert_dicts(c7, [dict(a=dict(a1=5, a2=6), b=3), dict(a=dict(a1=6, a2=5), b=3)])

if __name__ == "__main__":
    test_simple()
