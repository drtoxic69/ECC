# Definition of Field E(Z/pZ) for the elliptic curve : y^2 = x^3 + ax + b
#
# The Group operation for the curve are under the Field E(Z/pZ).
# The operations like : - Addition       (+)
#                       - Multiplication (*)
#                       - Subtraction    (-)
#
# For the operation   : - Power          (^)
#
# We use the Fermat's Little Theorem. As we have to compute a^k for all
# a and k are integers. We know that a^(p-1) = 1 (mod p) for all p = prime.
# Then :
#               a^m(p-1) = 1 (mod p)
#
# Let k be some integer such that k = q(p-1) + r.
#
#               a^k = a^(q(p-1) + r)    (mod p)
#               a^k = (a^(p-1))^q * a^r (mod p)
#               a^k = a^r               (mod p)
#               a^k = a^(k mod p-1)     (mod p)


class FieldElement:
    def __init__(self, num: int, prime: int):
        if num >= prime or num < 0:
            raise ValueError(f"{num} is not in Filed range 0 to {prime - 1}")

        self.num   = num
        self.prime = prime


    def __add__(self, other):
        if self.prime != other.prime:
            raise TypeError("Can not add the elements of different Field.")

        return FieldElement((self.num + other.num) % self.prime, self.prime)


    def __sub__(self, other):
        if self.prime != other.prime:
            raise TypeError("Can not subtract the elements of different Field.")

        return FieldElement((self.num - other.num) % self.prime, self.prime)


    def __mul__(self, other):
        if self.prime != other.prime:
            raise TypeError("Can not multiply the elements of different Field.")

        return FieldElement((self.num * other.num) % self.prime, self.prime)


    def __eq__(self, other):
        if other is None:
            return False

        return self.num == other.num and self.prime == other.prime

    def __rmul__(self, coefficient):
        res = (coefficient * self.num) % self.prime
        return FieldElement(res, self.prime)


    def __truediv__(self, other):
        if self.prime != other.prime:
            raise TypeError("Can not divide the elements of different Field.")

        inv = pow(other.num, -1, self.prime)
        num = (self.num * inv) % self.prime

        return FieldElement(num, self.prime)


    def __pow__(self, exponent: int):
        exponent = exponent % (self.prime - 1)
        return FieldElement(pow(self.num, exponent, self.prime), self.prime)


    def __repr__(self):
        return f"F_{self.prime}({self.num})"
