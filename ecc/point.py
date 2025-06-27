# Definition of Point on the curve : y^2 = x^3 + ax + b
#
# Group operation for the elliptic curve.
# The operations are:
#                   - Addition
#                   - Scalar Multiplication
#
# For Addition:
#
# Let's say we have two distinct point P and Q, we want
# to do P + Q, so we find the line passing through both
# the points P and Q, and this would intersect the curve
# at a point -R, we find the reflection of -R to get R.
# Such that :
#                      P + Q = R
#
# So, we find the slope of the line passing through P & Q.
#
#               s  = (yp - yq)/(xp - xq)
#               xr = s^2 - (xp + xq)
#               yr = s(xp - xr) - yp
#
# But, if P and Q are the same point, then we have to find
# 2P. To find 2P, we have to find the slope of the tangent
# at the point P, we can do that by finding the derivative
# of the curve.
#                     2P = P + P
#
# So, the derivative of the curve would be
#
#               s  = (3xp + a)/2yp
#               xr = s^2 - 2xp
#               yr = s(xp - xr) - yp
#
#
# For Scalar Multiplication:
#
# Let's say for a Point P in the curve and let there be a
# scalar k that belongs to Z. Then k * P is just adding P
# k times. We do this by Double and Add Algorithm.
#
#               Q = k * P
#               Q = P + P + ... + P (k times)


from .field import FieldElement


class Point:
    def __init__(self, x, y, curve):
        self.curve = curve
        self.prime = curve.P

        # Curve parameters: y^2 = x^3 + ax + b
        self.a = FieldElement(curve.a, self.prime)
        self.b = FieldElement(curve.b, self.prime)

        if not x and not y:
            self.x, self.y = None, None
        else:
            self.x = FieldElement(x, self.prime)
            self.y = FieldElement(y, self.prime)

            if self.y**2 != self.x**3 + self.a * self.x + self.b:
                raise ValueError(f"Point({x}, {y}) is not on the curve.")


    def __add__(self, other):
        if self.curve != other.curve:
            raise TypeError("Points are not on the same curve.")

        # Identity case
        if self.x is None:
            return other
        if other.x is None:
            return self

        # Point at infinity
        if self.x == other.x and self.y != other.y:
            return Point(None, None, self.curve)

        # Distinct Points
        if self.x != other.x:
            s  = (other.y - self.y) / (other.x - self.x)
            xr = s**2 - (self.x + other.x)
            yr = s * (self.x - xr) - self.y

            return Point(xr.num, yr.num, self.curve)

        # Point doubling
        if self == other:
            s  = (3 * self.x**2 + self.a) / (2 * self.y)
            xr = s**2 - 2 * self.x
            yr = s * (self.x - xr) - self.y

            return Point(xr.num, yr.num, self.curve)

        return Point(None, None, self.curve)


    def __eq__(self, other):
        if not isinstance(other, Point):
            return False

        return self.x == other.x and self.y == other.y and self.curve == other.curve


    def __rmul__(self, coefficient):
        result = Point(None, None, self.curve)
        addend = self

        # Double and Add Algorithm
        while coefficient:
            if coefficient & 1:
                result = result + addend
            addend = addend + addend
            coefficient >>= 1

        return result


    def __repr__(self):
        if self.x is None:
            return "Point(infinity)"

        return f"Point(\n\t{self.x.num}, \n\t{self.y.num}\n)"
