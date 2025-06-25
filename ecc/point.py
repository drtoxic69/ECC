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
            xr = s ** 2 - (self.x + other.x)
            yr = s * (self.x - xr) - self.y

            return Point(xr.num, yr.num, self.curve)

        # Point doubling
        if self == other:
            s  = (3 * self.x**2 + self.a) / (2 * self.y)
            xr = s ** 2 - 2 * self.x
            yr = s * (self.x - xr) - self.y

            return Point(xr.num, yr.num, self.curve)

        return Point(None, None, self.curve)


