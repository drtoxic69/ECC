# Definition of the Elliptic Curve.
#
# First, we check if the curve is singular, meaning if the
# discriminant of the curve is 0. We discard such curves
# because if the discriminant is 0, it means the curve has
# cusps or self-intersection. We do not use such curves in
# cryptography.
#
# For any polynomial, the discriminant gives the criterion
# for whether the polynomial has repeated roots or not.
#
# For a cubic polynomial:
#               f(x) = (x - α)(x - β)(x - γ)
#
# Therefore, the discriminant is given by,
#               ∆ = a^4 (α−β)^2 (β−γ)^2 (γ−α)^2
#
# So, for a Elliptic curve in defined by the short Weierstrass
# form:
#               y^2 = x^3 + ax + b
#
# Full discriminant formula:
#               ∆ = -16(4a^3 + 27b^2)
#
#
# Elliptic Curve Discreate Logarithmic Problem:
#
# Scalar Muiltiplication -> one way function
# over the Field E(Z/pZ)
#
# Let there be a point G such that G belongs to E(Z/pZ) and
# G generates all the points in the Field E(Z/pZ).
#
# So, we can say that the Co-factor,
#
#               h = |E(Z/pZ)|/n where n = ord(G)
#
# Usually we select G such that h = 1.
#
# So, Therefore, the Domain parameters are {P, a, b, G, n, h}.
# The domain parameters are public.


class Curve:
    def __init__(self, a, b, P, G, n, h=1):
        """
        parameters:
        a, b    : Curve parameters (y^2 = x^3 + ax + b).
        P       : Prime modulo for finite Field.
        G       : Generator point.
        n       : Order of Generator point.
        h       : Co-factor (usually 1).
        """

        self.a = a
        self.b = b

        self.P = P
        self.G = G
        self.n = n

        # Check if the curve is singular
        if 4 * (a**2) + 27 * (b**2) == 0:
            raise ValueError(
                "This is a singular curve (discriminant is zero). Choose different parameters for the curve."
            )

    def __repr__(self):
        return f"Curve: y^2 = x^3 + {self.a}x + {self.b} over the Field(Z/{self.P}Z)."
