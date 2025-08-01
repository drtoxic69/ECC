"""
This module provides classes for generating and managing elliptic curve key pairs.

A key pair consists of a private key (a secret integer) and a public key
(a point on the curve derived from the private key).

Private Key - A random number (k) in between 1 and n, where n is order of
              generator point G.

Public Key - The point P = k * G, on the elliptic curve with Field E(Z/pZ)
"""

from __future__ import annotations
from functools import cached_property
from secrets import randbelow

from .curve import Curve
from .point import Point


class PublicKey:
    """Represents an elliptic curve public key, which is a point on the curve."""

    def __init__(self, point: Point):
        """Initializes a PublicKey from a Point object."""
        self.point = point

    @property
    def curve(self) -> Curve:
        """Dynamic shortcut to curve."""
        return self.point.curve

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PublicKey):
            return NotImplemented
        return self.point == other.point

    def __repr__(self):
        if (self.point.x, self.point.y) == (None, None):
            return "PublicKey(Point(infinity))"
        return (
            f"PublicKey(\n\tx={hex(self.point.x.num)}, \n\ty={hex(self.point.y.num)}\n)"
        )


class PrivateKey:
    """Represents an elliptic curve private key, which is a secret integer."""

    def __init__(self, secret: int | None = None, *, curve: Curve):
        """
        Generates or wraps a private key for a given curve.

        Args:
            secret: The private key integer. If None, a new one is generated.
            curve: The elliptic curve to use. Must be provided as a keyword argument.
        """
        self.curve = curve

        if secret is None:
            self.secret = randbelow(curve.n - 1) + 1
        else:
            if not (1 <= secret < curve.n):
                raise ValueError(f"PrivateKey must be in between 1 and {curve.n - 1}.")
            self.secret = secret

    @cached_property
    def public_key(self) -> PublicKey:
        """The corresponding public key, calculated as P = secret * G."""
        public_point = self.secret * self.curve.G
        return PublicKey(public_point)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PrivateKey):
            return NotImplemented

        return self.secret == other.secret and self.curve == other.curve

    def __repr__(self) -> str:
        return "PrivateKey(secret=...)"


def generate_keypair(curve: Curve) -> tuple[PrivateKey, PublicKey]:
    """Generates a (private_key, public_key) pair for a given curve."""
    private_key = PrivateKey(curve=curve)
    public_key = private_key.public_key

    return private_key, public_key
