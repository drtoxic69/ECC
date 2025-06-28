from secrets import randbelow
from .point import Point


class PublicKey:
    def __init__(self, point: Point, curve):
        if not isinstance(point, Point):
            raise TypeError("Public Key must be a Point.")

        self.point = point
        self.curve = curve


    def __repr__(self):
        return f"PublicKey(\n\tx={hex(self.point.x.num)}, \n\ty={hex(self.point.y.num)}\n)"


class PrivateKey:
    def __init__(self, secret=None, curve=None):
        if curve is None:
            raise ValueError("Curve must be specified.")

        self.curve = curve

        if secret is None:
            self.secret = randbelow(curve.n - 1) + 1

        else:
            if secret not in range(1, curve.n):
                raise ValueError(f"PrivateKey must be in between 1 and {curve.n - 1}.")

            self.secret = secret

        self._public_key = None


    def public_key(self):
        if self._public_key is None:

            Gx, Gy = self.curve.G
            G = Point(Gx, Gy, self.curve)
            p = self.secret * G

            self._public_key = PublicKey(p, self.curve)

        return self._public_key


    def __repr__(self):
        return f"PrivateKey=({self.secret})"


def generate_keypair(curve):
    """Generates a (private_key, public_key) pair for a given curve. """
    private_key = PrivateKey(curve=curve)
    public_key  = private_key.public_key()

    return private_key, public_key
