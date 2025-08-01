from hypothesis import given, strategies as st
from ecc import secp256k1
from ecc import PrivateKey


class TestSecp256k1Integration:
    """
    Integration tests for the secp256k1 curve instance.
    These tests verify that the library works correctly with standard,
    real-world curve parameters and known test vectors.
    """

    def test_generator_is_on_curve(self):
        """The secp256k1 generator point G must satisfy the curve equation."""
        G = secp256k1.G
        assert G is not None, "Generator point should not be None"
        assert G.y**2 == G.x**3 + secp256k1.a * G.x + secp256k1.b

    def test_point_order_is_correct(self):
        """The order 'n' of the curve should result in n * G = Infinity."""
        G = secp256k1.G
        n = secp256k1.n
        infinity_point = n * G

        assert infinity_point.x is None, (
            "The x-coordinate should be None for the point at infinity"
        )
        assert infinity_point.y is None, (
            "The y-coordinate should be None for the point at infinity"
        )

    def test_known_scalar_multiplication(self):
        """
        Known Answer Test (KAT): Verifies scalar multiplication against a
        standard, pre-computed value for 2*G on secp256k1.
        """
        G = secp256k1.G
        two_G = 2 * G

        two_G_x = 0xC6047F9441ED7D6D3045406E95C07CD85C778E4B8CEF3CA7ABAC09B95C709EE5
        two_G_y = 0x1AE168FEA63DC339A3C58419466CEAEEF7F632653266D0E1236431A950CFE52A

        assert two_G.x.num == two_G_x
        assert two_G.y.num == two_G_y


# --- Property-Based Testing for Secp256k1 ---

secp256k1_secrets = st.integers(min_value=1, max_value=secp256k1.n - 1)


@given(k=secp256k1_secrets)
def test_multiplicative_inverse_property(k):
    """
    Property: For any scalar k, k * G * k⁻¹ should result back in G.
    This is a strong check of the entire multiplication and field logic.
    """
    G = secp256k1.G
    P = k * G
    k_inv = pow(k, -1, secp256k1.n)
    G_check = k_inv * P

    assert G_check == G


@given(secret=secp256k1_secrets)
def test_generated_public_key_is_valid(secret):
    """
    Property: A public key generated from any valid secret must be a
    valid point on the curve.
    """
    private_key = PrivateKey(secret=secret, curve=secp256k1)
    point = private_key.public_key.point

    assert point.y**2 == point.x**3 + secp256k1.a * point.x + secp256k1.b
