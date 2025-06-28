import hashlib
from secrets import randbelow

from .point import Point
from .keys import PublicKey, PrivateKey


class Signature:
    """Represents an ECDSA signature (r, s)."""
    def __init__(self, r: int, s: int):
        self.r = r
        self.s = s

    def __repr__(self):
        return f"<Signature \n\tr=0x{self.r:x}, \n\ts=0x{self.s:x}\n>"


def _hash_msg(message: bytes, n: int) -> int:
    """
    Hashes the message with SHA-256 and truncates to 
    modulo n to produce an integer in [0, n-1].
    """
    h = hashlib.sha256(message).digest()
    z = int.from_bytes(h, 'big')

    return z % n


def sign(message: bytes, private: PrivateKey) -> Signature:
    """
    Generate an ECDSA signature on 'message' using 'private' (PrivateKey).
    Returns a Signature(r, s).
    """
    curve  = private.curve
    n      = curve.n
    Gx, Gy = curve.G
    
    z = _hash_msg(message, n)
    G = Point(Gx, Gy, curve)

    while True:
        # Generate nonce k [1, n-1]
        k = randbelow(n-1) + 1

        # Compute for r
        R = k * G
        r = R.x.num % n

        if r == 0:
            continue
        
        # Compute s = k^-1(z + rp) mod n
        k_inv = pow(k, -1, n)
        s = (k_inv * (z + r * private.secret)) % n

        if s == 0:
            continue

        return Signature(r, s)


def verify(message: bytes, sign: Signature, public: PublicKey) -> bool:
    """
    Verify an ECDSA 'sign' on 'message' using the public key 'public'.
    Returns True if valid, False otherwise.
    """
    curve  = public.curve
    n      = curve.n
    Gx, Gy = curve.G
    
    r, s = sign.r, sign.s 
    
    # Check if s and r in between 1 and n-1
    if not (1 <= r < n and 1 <= s < n):
        return False

    z = _hash_msg(message, n)
    s_inv = pow(s, -1, n)

    # Compute u1 = z·s⁻¹ mod n, u2 = r·s⁻¹ mod n
    u1 = (z * s_inv) % n
    u2 = (r * s_inv) % n

    # Compute P = u1*G + u2*Q
    G = Point(Gx, Gy, curve)
    P = u1 * G + u2 * public.point
    
    if P.x is None:
        return False

    return (P.x.num % n) == r


