# Generation of Private Key and Public Key.
#
# Private Key - A random number (k) in between 1 and n,
#               where n is order of generator point G.
#
# Public Key - The point P = k * G, on the elliptic
#              curve with Field E(Z/pZ)
#
# Here, we use the randbelow function from secrets
# to get a random number in between 1 and n(curve.n).
# Here, n is ord(G). G is the generator point, and
# ord(n) is the no. of points G can generate. Usually
# n is |E(Z/pZ)|, as we choose the generator point to
# get all the points in the Field E(Z/pZ).
#
# The random number we get is our Private Key. And we
# multiply the random number with the generator point
# G to get our Public Key.
#
#       secret -> random number between (1, n)
#       public_key -> point
#
#       private_key = PrivateKey(secret, curve)
#
#       public_key = private_key.public_key()
#       public_key = secret * G


from secrets import randbelow
from .point import Point


class PublicKey:
    def __init__(self, point: Point, curve):
        self.point = point
        self.curve = curve


    def __repr__(self):
        if (self.point.x, self.point.y) == (None, None):
            return "PublicKey(Point(infinity))"
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
