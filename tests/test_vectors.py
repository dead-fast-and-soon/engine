
from konkyo.structs.vector import Vector

vec = Vector(0, 0)


def test_comparisons():

    assert vec == (0, 0)
    assert vec == Vector(0, 0)


def test_operations():

    assert vec + (1, 1) == (1, 1)
    assert vec + Vector(1, 1) == (1, 1)

    assert Vector(1, 1) * 2 == (2, 2)
