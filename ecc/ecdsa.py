"""
This module implements the core logic for the Elliptic Curve Digital Signature
Algorithm (ECDSA), including deterministic nonce generation as specified in
RFC 6979.
"""

import hashlib
import hmac


class Signature:
    """Represents an ECDSA signature, consisting of two integers (r, s)."""

    def __init__(self, r: int, s: int):
        self.r = r
        self.s = s

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Signature):
            return NotImplemented
        return self.r == other.r and self.s == other.s

    def __repr__(self) -> str:
        return f"Signature(\n\tr=0x{self.r:x}, \n\ts=0x{self.s:x}\n)"


def _rfc6979_nonce(secret: int, n: int, message_hash: bytes) -> int:
    """
    Generates a deterministic nonce 'k' as per RFC 6979.
    This is safer than using a random number generator.
    """
    hash_len = 32  # For SHA-256

    # Set values for HMAC key 'K' and value to hash 'V'
    V = b"\x01" * hash_len
    K = b"\x00" * hash_len

    # Private Key in bytes
    private_key = secret.to_bytes(hash_len, "big")

    K = hmac.new(K, V + b"\x00" + private_key + message_hash, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()
    K = hmac.new(K, V + b"\x01" + private_key + message_hash, hashlib.sha256).digest()
    V = hmac.new(K, V, hashlib.sha256).digest()

    while True:
        V = hmac.new(K, V, hashlib.sha256).digest()
        k = int.from_bytes(V, "big")

        if 1 <= k < n:
            return k

        K = hmac.new(K, V + b"\x00", hashlib.sha256).digest()
        V = hmac.new(K, V, hashlib.sha256).digest()
