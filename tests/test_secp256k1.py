from ecc import Point
from ecc import secp256k1


def test_generator_point():
    Gx, Gy = secp256k1.G
    G = Point(Gx, Gy, secp256k1)
    assert G


def test_scalar_multiplication():
    Gx, Gy = secp256k1.G
    G = Point(Gx, Gy, secp256k1)

    k = 2
    P = k * G

    k_inv = pow(k, -1, secp256k1.n)
    G_check = k_inv * P

    assert G_check == G


