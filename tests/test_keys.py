from ecc import Curve
from ecc import Point
from ecc import secp256k1
from ecc import PrivateKey, PublicKey, generate_keypair


curve = Curve(2, 2, 17, (5, 1), 19)

def test_private_key_with_secrt():
    secret = 10
    private = PrivateKey(secret, curve)

    assert private.secret == secret


def test_public_key_with_points():
    point = Point(5, 1, curve)
    public = PublicKey(point, curve)

    assert public.point == point


def test_private_key_generation():
    private = PrivateKey(curve=curve)

    assert private.secret in range(1, curve.n)


def test_cacheing():
    private = PrivateKey(curve=curve)

    pub_key1 = private.public_key()
    pub_key2 = private.public_key()
    
    assert pub_key1 is pub_key2

def test_generate_keypair():
    private, public = generate_keypair(curve)

    assert private.public_key() == public


def test_keypair_generation_secp256k1():
    private, public = generate_keypair(secp256k1)

    assert private.secret in range(1, secp256k1.n)

    point = public.point
    if (point.x, point.y) != (None, None):
        assert point.y**2 == point.x**3 + point.a * point.x + point.b
