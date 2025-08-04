"""
Implements Elliptic Curve Diffie-Hellman (ECDH) key exchange using a
standard Key Derivation Function (KDF) based on HKDF (RFC 5869).
"""

from __future__ import annotations

import hashlib
import hmac
import typing

if typing.TYPE_CHECKING:
    from .keys import PrivateKey, PublicKey


def generate_shared_secret(
    private_key: PrivateKey,
    public_key: PublicKey,
    hash_alg=hashlib.sha256,
    salt: bytes | None = None,
    info: bytes = b"",
    key_length: int = 32,
) -> bytes:
    """
    Computes the ECDH shared secret using an HKDF-like construction.

    Args:
        private_key : The local party's private key.
        public_key  : The remote party's public key.
        hash_alg    : The hash algorithm to use for the KDF.
        salt        : An optional non-secret random value for the KDF.
        info        : Optional context-specific information for the KDF.
        key_length  : The desired length of the output key in bytes.

    Returns:
        A cryptographically strong shared key of the specified length.
    """
    if private_key.curve != public_key.curve:
        raise ValueError("Keys must be on the same curve for ECDH.")

    # 1. The core ECDH calculation
    shared_point = private_key.secret * public_key.point

    assert shared_point.x is not None
    raw_shared_secret = shared_point.x.num.to_bytes(32, "big")

    # 2. HKDF-Extract: Create a strong pseudorandom key from the raw secret.
    # The salt is optional but highly recommended.
    if salt is None:
        hmac_salt = b"\x00" * hash_alg().digest_size
    else:
        hmac_salt = salt

    prk = hmac.new(hmac_salt, raw_shared_secret, hash_alg).digest()

    # 3. HKDF-Expand: Generate the final key material.
    okm = b""
    t = b""
    for i in range((key_length + hash_alg().digest_size - 1) // hash_alg().digest_size):
        t = hmac.new(prk, t + info + bytes([i + 1]), hash_alg).digest()
        okm += t

    return okm[:key_length]
