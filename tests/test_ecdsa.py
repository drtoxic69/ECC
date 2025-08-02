from hypothesis import given
from hypothesis import strategies as st

from ecc import PrivateKey, Signature, generate_keypair, secp256k1

# --- Official RFC 6979 Test Vector for secp256k1 ---
# Source: RFC 6979, Appendix A.2.5
KAT_D = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
KAT_MSG = b"sample"
KAT_R = 0x432310E32CB80EB6503A26CE83CC165C783B870845FB8AAD6D970889FCD7A6C8
KAT_S = 0x530128B6B81C548874A6305D93ED071CA6E05074D85863D4056CE89B02BFAB69


class TestECDSACorrectness:
    """Verifies the ECDSA implementation against the official RFC 6979 standard."""

    def test_known_answer_vector_rfc6979(self):
        """
        Tests the implementation against the official test vector from
        RFC 6979, Appendix A.2.5. This is the gold standard for correctness.
        """
        private_key = PrivateKey(secret=KAT_D, curve=secp256k1)
        public_key = private_key.public_key

        # 1. Test Signature Generation
        signature = private_key.sign(KAT_MSG)
        assert signature.r == KAT_R, (
            "The 'r' component does not match the official RFC 6979 vector."
        )
        assert signature.s == KAT_S, (
            "The 's' component does not match the official RFC 6979 vector."
        )

        # 2. Test Signature Verification
        assert public_key.verify(KAT_MSG, signature) is True, (
            "A valid known signature failed to verify."
        )


class TestECDSASecurity:
    """Tests for fundamental security properties."""

    def test_sign_produces_low_s_signature(self):
        """The sign function must enforce a low-s value to prevent malleability."""
        private_key = PrivateKey(curve=secp256k1)
        signature = private_key.sign(b"test for low-s")
        assert signature.s <= secp256k1.n // 2

    def test_verify_accepts_high_s_signature(self):
        """The verify function must accept a mathematically valid high-s signature."""
        priv, pub = generate_keypair(secp256k1)
        message = b"test for malleability"
        low_s_signature = priv.sign(message)

        high_s = secp256k1.n - low_s_signature.s
        malleated_signature = Signature(r=low_s_signature.r, s=high_s)

        assert pub.verify(message, malleated_signature) is True


# --- Property-Based Testing ---

private_keys = st.builds(PrivateKey, curve=st.just(secp256k1))
messages = st.binary(min_size=1, max_size=256)


@given(private_key=private_keys, message=messages)
def test_sign_verify_property(private_key, message):
    """Property: Any message signed by a key must be verifiable by its public key."""
    public_key = private_key.public_key
    signature = private_key.sign(message)
    assert public_key.verify(message, signature) is True


@given(private_key=private_keys, message=messages)
def test_deterministic_signature_property(private_key, message):
    """Property: Signing the same message twice must produce the exact same signature."""
    sig1 = private_key.sign(message)
    sig2 = private_key.sign(message)
    assert sig1 == sig2
