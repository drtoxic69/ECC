"""
This module provides classes for generating and managing elliptic curve key pairs.

Provides classes for generating and managing elliptic curve key pairs.
Includes methods for creating and verifying digital signatures.

A key pair consists of a private key (a secret integer) and a public key
(a point on the curve derived from the private key).

Private Key - A random number (k) in between 1 and n, where n is order of
              generator point G.

Public Key - The point P = k * G, on the elliptic curve with Field E(Z/pZ)
"""

from __future__ import annotations

import hashlib
from functools import cached_property
from secrets import randbelow

from .curve import Curve
from .ecdsa import Signature, _rfc6979_nonce
from .point import Point


class PublicKey:
    """Represents an elliptic curve public key."""

    def __init__(self, point: Point):
        self.point = point

    @property
    def curve(self) -> Curve:
        """A convenient, read-only shortcut to the key's curve."""
        return self.point.curve

    def verify(self, message: bytes, signature: Signature) -> bool:
        """Verifies an ECDSA signature for a given message."""
        n = self.curve.n
        r, s = signature.r, signature.s

        # 1. First check if the r and s are vaild, by checking if they are in the range[1, n]
        if not (1 <= r < n and 1 <= s < n):
            return False

        # 2. Hash the message to get the integer 'z'
        z = int.from_bytes(hashlib.sha256(message).digest(), "big")
        s_inv = pow(s, -1, n)

        u1 = (z * s_inv) % n
        u2 = (r * s_inv) % n

        # 3. calculate P = u1 * G + u2 * PublicKey, and check P.x == r
        P = (u1 * self.curve.G) + (u2 * self.point)

        if P.x is None:
            return False

        return P.x.num % n == r

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PublicKey):
            return NotImplemented

        return self.point == other.point

    def __repr__(self) -> str:
        if self.point.x is None or self.point.y is None:
            return "PublicKey(Point(infinity))"

        return f"PublicKey(\n\tx=0x{self.point.x.num:x}, \n\ty=0x{self.point.y.num:x})"


class PrivateKey:
    """Represents an elliptic curve private key."""

    def __init__(self, secret: int | None = None, *, curve: Curve):
        self.curve = curve

        if secret is None:
            self.secret = randbelow(curve.n - 1) + 1

        else:
            if not (1 <= secret < curve.n):
                raise ValueError(f"Secret must be in the range [1, {curve.n - 1}].")
            self.secret = secret

    @cached_property
    def public_key(self) -> PublicKey:
        """The corresponding public key, calculated efficiently on first access."""
        return PublicKey(self.secret * self.curve.G)

    def sign(self, message: bytes) -> Signature:
        """Generates an ECDSA signature for a given message."""
        n = self.curve.n

        # These are the steps to follow:
        # 1. Hash the message to get the integer 'z'
        z = int.from_bytes(hashlib.sha256(message).digest(), "big")

        # 2. The RFC 6979 nonce function requires the raw hash digest
        message_hash = z.to_bytes(32, "big")

        # This loop is for the rare case that r or s is zero
        while True:
            # 3. Generate the nonce `k` using the correctly formatted hash
            k = _rfc6979_nonce(self.secret, n, message_hash)

            R = k * self.curve.G

            if R.x is None:
                continue

            r = R.x.num % n
            if r == 0:
                continue

            k_inv = pow(k, -1, n)
            s = (k_inv * (z + r * self.secret)) % n
            if s == 0:
                continue

            # Enforce low-s value for non-malleability
            if s > n // 2:
                s = n - s

            return Signature(r, s)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PrivateKey):
            return NotImplemented

        return self.secret == other.secret and self.curve == other.curve

    def __repr__(self) -> str:
        return "PrivateKey(secret=...)"


def generate_keypair(curve: Curve) -> tuple[PrivateKey, PublicKey]:
    """A helper function to generate a new key pair on a given curve."""
    private_key = PrivateKey(curve=curve)
    public_key = private_key.public_key
    return private_key, public_key
