import pytest
from hypothesis import given
from hypothesis import strategies as st

from ecc import Curve, PrivateKey, generate_keypair, generate_shared_secret, secp256k1

# --- Test Class for Organization ---


class TestECDH:
    """Tests the Elliptic Curve Diffie-Hellman key exchange implementation."""

    def test_shared_secret_agreement(self):
        """
        Tests the fundamental property of ECDH: two parties must arrive
        at the exact same shared secret.
        """
        # 1. Alice generates her key pair
        alice_priv, alice_pub = generate_keypair(secp256k1)

        # 2. Bob generates his key pair
        bob_priv, bob_pub = generate_keypair(secp256k1)

        # 3. Alice computes the shared secret using her private key and Bob's public key.
        secret_by_alice = generate_shared_secret(alice_priv, bob_pub)

        # 4. Bob computes the shared secret using his private key and Alice's public key.
        secret_by_bob = generate_shared_secret(bob_priv, alice_pub)

        # 5. The secrets must be identical and have the correct length.
        assert len(secret_by_alice) == 32
        assert secret_by_alice == secret_by_bob

    def test_ecdh_fails_with_different_curves(self):
        """
        Tests that the ECDH exchange raises a ValueError if the keys
        are not on the same curve.
        """
        # Create a small toy curve for the test
        toy_curve = Curve(a=2, b=2, P=17, G=(5, 1), n=19)

        alice_priv, _ = generate_keypair(secp256k1)
        _, bob_pub = generate_keypair(toy_curve)

        with pytest.raises(
            ValueError, match="Keys must be on the same curve for ECDH."
        ):
            generate_shared_secret(alice_priv, bob_pub)

    def test_kdf_produces_different_keys_with_different_info(self):
        """
        Tests that the HKDF correctly produces different keys when the
        'info' parameter is different.
        """
        alice_priv, _ = generate_keypair(secp256k1)
        _, bob_pub = generate_keypair(secp256k1)

        # Generate a key for one context
        secret1 = alice_priv.ecdh(bob_pub, info=b"for encryption")

        # Generate a key for a different context
        secret2 = alice_priv.ecdh(bob_pub, info=b"for authentication")

        assert secret1 != secret2


# --- Property-Based Testing ---

# A strategy to generate a valid private key for secp256k1
private_keys = st.builds(PrivateKey, curve=st.just(secp256k1))


@given(alice_priv=private_keys, bob_priv=private_keys)
def test_shared_secret_agreement_property(alice_priv, bob_priv):
    """
    Property: For any two generated key pairs, both parties must
    always arrive at the same shared secret.
    """
    alice_pub = alice_priv.public_key
    bob_pub = bob_priv.public_key

    secret_by_alice = alice_priv.ecdh(bob_pub)
    secret_by_bob = bob_priv.ecdh(alice_pub)

    assert secret_by_alice == secret_by_bob
