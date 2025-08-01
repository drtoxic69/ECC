"""
This module defines the Point class for elliptic curve cryptography.

It includes the implementation of elliptic curve group operations such
as point addition and constant-time scalar multiplication using a
Montgomery Ladder to protect against side-channel attacks.

Definition of Point on the curve : y² = x³ + ax + b

Group operation for the elliptic curve.
The operations are:
                  - Addition
                  - Scalar Multiplication

"""

from __future__ import annotations
from .field import FieldElement


class Point:
    """
    Represents a point on a specific elliptic curve.

    Point(x, y, curve) is a point (x, y) defined over a finite
    field E(Z/pZ) on the 'curve'. The specified curve has curve
    parameters (a, b) and a prime modulo P.
    """

    def __init__(self, x: int, y: int | None, curve):
        """
        Arguments:
            x, y    : (x, y) on the curve over the Field E(Z/pZ)
            curve   : Elliptic curve over the Field E(Z/pZ)
        """
        self.curve = curve

        if x is None and y is None:
            self.x, self.y = None, None
        else:
            self.x = FieldElement(x, curve.P)
            self.y = FieldElement(y, curve.P)

            if self.y**2 != self.x**3 + curve.a * self.x + curve.b:
                raise ValueError(f"Point({x}, {y}) is not on the curve.")

    def __add__(self, other) -> "Point":
        """Performs elliptic curve point addition.

        Let's say we have two distinct point P and Q, we want
        to do P + Q, so we find the line passing through both
        the points P and Q, and this would intersect the curve
        at a point -R, we find the reflection of -R to get R.
        Such that :
                             P + Q = R

        But, if P and Q are the same point, then we have to find
        2P. To find 2P, we have to find the slope of the tangent
        at the point P, we can do that by finding the derivative
        of the curve.
                            2P = P + P
        """
        if self.curve != other.curve:
            raise TypeError("Points are not on the same curve.")

        # Identity case: if one of the points is the point at infinity
        if self.x is None:
            return other
        if other.x is None:
            return self

        # Checks for Point doubling and additive inverses
        if self.x == other.x:
            # Additive inverses case: (P) + (-P) = infinity
            # y-coordinates is different
            if self.y != other.y:
                return Point(None, None, self.curve)

            # Point doubling case: P + P = 2P
            # If the denominator of the slope, 2 * y = 0, then the
            # tangent would be a vertical line
            if self.y.num == 0:
                return Point(None, None, self.curve)

            # Calculate slope of the tangent: s = (3x² + a) / 2y
            s = (3 * self.x**2 + self.curve.a) / (2 * self.y)

        else:
            # Standard Point Addition case: P + Q = R
            # s = (y₂ - y₁) / (x₂ - x₁)
            s = (other.y - self.y) / (other.x - self.x)

        # xr = s² - (x₁ + x₂)
        xr = s**2 - (self.x + other.x)

        # yr = s(x₁ - xr) - y₁
        yr = s * (self.x - xr) - self.y

        return Point(xr.num, yr.num, self.curve)

    def __rmul__(self, scalar: int) -> Point:
        """
        Constant-time scalar multiplication using a secure Montgomery ladder.

        Let's say for a Point P in the curve and let there be a scalar k that
        belongs to Z. Then k * P is just adding P k times.

                      Q = k * P
                      Q = P + P + ... + P (k times)

        We do this by Montgomery ladder, cause it is safer from Timing
        Side-Channel Attacks.
        """
        if not isinstance(scalar, int):
            raise TypeError("Scalar must be an integer.")

        R0 = Point(None, None, self.curve)  # R0 -> point at infinity
        R1 = self

        # Fixed number of times the loop runs
        for i in range(255, -1, -1):
            bit = (scalar >> i) & 1

            if bit:
                R0, R1 = R1, R0

            R1 = R0 + R1
            R0 = R0 + R0

            if bit:
                R0, R1 = R1, R0

        return R0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __repr__(self):
        if self.x is None:
            return "Point(infinity)"

        return f"Point(\n\t{self.x.num}, \n\t{self.y.num}\n)"
