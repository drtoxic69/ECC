"""
This module defines the Curve class, representing an elliptic curve
in the short Weierstrass form.
"""

from __future__ import annotations
from functools import cached_property

from .field import FieldElement
from .point import Point


class Curve:
    """Represents an elliptic curve y² = x³ + ax + b over a finite field Fp or E(Z/pZ)."""

    def __init__(
        self,
        a: int,
        b: int,
        P: int,
        G: tuple[int, int],
        n: int,
        h: int = 1,
        name: str = None,
    ):
        """
        parameters:
        a, b    : Curve parameters (y^2 = x^3 + ax + b).
        P       : Prime modulo for finite Field.
        G       : Generator point.
        n       : Order of Generator point.
        h       : Co-factor (usually 1).
        name    : Name of the curve. (optional)
        """

        self.a = FieldElement(a, P)
        self.b = FieldElement(b, P)

        self.P = P
        self.n = n
        self.h = h
        self.name = name

        self._G = G

        # Check if the curve is singular
        if 4 * (a**3) + 27 * (b**2) == 0:
            raise ValueError(
                "This is a singular curve (discriminant is zero). Choose different parameters for the curve."
            )

    @cached_property
    def G(self) -> Point:
        return Point(x=self._G[0], y=self._G[1], curve=self)

    def __repr__(self) -> str:
        if self.name:
            return f"Curve({self.name})"
        return f"Curve(y² = x³ + {self.a.num}x + {self.b.num} mod {self.P})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Curve):
            return NotImplemented

        return (
            self.P == other.P
            and self.a == other.a
            and self.b == other.b
            and self._G == other._G
        )
