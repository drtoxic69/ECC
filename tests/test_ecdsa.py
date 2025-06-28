from ecc import secp256k1
from ecc import generate_keypair
from ecc import sign, verify, Signature


def test_sign_and_verify():
    priv, pub = generate_keypair(secp256k1)
    message = b"Hello, World"
    sig = sign(message, priv)

    assert isinstance(sig, Signature)
    assert verify(message, sig, pub)


def test_sign_with_different_priv():
    priv1, _ = generate_keypair(secp256k1)
    priv2, _ = generate_keypair(secp256k1)

    message = b"test, :)"
    sig1 = sign(message, priv1)
    sig2 = sign(message, priv2)

    assert sig1.r != sig2.r or sig1.s != sig2.s


def test_sign_with_different_pub():
    priv1, pub1 = generate_keypair(secp256k1)
    priv2, pub2 = generate_keypair(secp256k1)

    message = b"test, :D"
    sig = sign(message, priv1)

    assert verify(message, sig, pub1)
    assert not verify(message, sig, pub2)


