from ecc import Point
from ecc import Curve
from ecc import FieldElement


G = (5, 1)
P = 17
n = 19

curve = Curve(2, 2, P, G, n)

def test_point_on_curve():
    p = Point(3, 1, curve)
    assert p.y**2 == p.x**3 + p.a * p.x + p.b


def test_addition():
    p1 = Point(5, 1, curve)
    p2 = Point(6, 3, curve)

    assert Point(10, 6, curve) == p1 + p2


def test_point_doubling():
    p = Point(5, 1, curve)
    assert Point(6, 3, curve) == p + p


def test_scalar_multiplication():
    p = Point(5, 1, curve)
    k = 16

    assert Point(10, 11, curve) == k * p


def test_infinity():
    p = Point(5, 1, curve)
    assert Point(None, None, curve) == n * p


