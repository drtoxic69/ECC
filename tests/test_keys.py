import pytest
from hypothesis import given
from hypothesis import strategies as st

from ecc import Curve, Point, PrivateKey, PublicKey, generate_keypair, secp256k1

# --- Test Setup ---
curve = Curve(P=17, a=2, b=2, G=(5, 1), n=19)


# --- Test Classes for Organization ---
class TestPrivateKey:
    """Tests functionalities of the PrivateKey class."""

    def test_init_with_secret(self):
        """Test creating a private key with a specific secret."""
        pk = PrivateKey(secret=10, curve=curve)
        assert pk.secret == 10
        assert pk.curve == curve

    def test_init_without_secret(self):
        """Test that a new key is generated within the correct range."""
        pk = PrivateKey(curve=curve)
        assert 1 <= pk.secret < curve.n

    def test_public_key_property(self):
        """Test that the public_key property computes the correct point."""
        pk = PrivateKey(secret=2, curve=curve)
        expected_point = Point(6, 3, curve)
        assert pk.public_key.point == expected_point

    def test_public_key_is_cached(self):
        """Test that the public key is computed only once and cached."""
        pk = PrivateKey(curve=curve)
        pub_key1 = pk.public_key
        pub_key2 = pk.public_key
        assert pub_key1 is pub_key2

    def test_equality(self):
        """Test the __eq__ method for private keys."""
        pk1 = PrivateKey(secret=5, curve=curve)
        pk2 = PrivateKey(secret=5, curve=curve)
        pk3 = PrivateKey(secret=6, curve=curve)
        assert pk1 == pk2
        assert pk1 != pk3


class TestPublicKey:
    """Tests functionalities of the PublicKey class."""

    def test_init(self):
        point = Point(5, 1, curve)
        pub_key = PublicKey(point)
        assert pub_key.point == point

    def test_curve_property(self):
        """Test that the curve property correctly points to the curve."""
        point = Point(5, 1, curve)
        pub_key = PublicKey(point)
        assert pub_key.curve == curve

    def test_equality(self):
        """Test the __eq__ method for public keys."""
        p1 = Point(5, 1, curve)
        p2 = Point(6, 3, curve)

        pub1 = PublicKey(p1)
        pub2 = PublicKey(p1)
        pub3 = PublicKey(p2)

        assert pub1 == pub2
        assert pub1 != pub3


class TestKeyGeneration:
    """Tests the key generation process and error handling."""

    def test_generate_keypair_function(self):
        """Test the top-level generate_keypair helper function."""
        private_key, public_key = generate_keypair(curve)

        assert isinstance(private_key, PrivateKey)
        assert isinstance(public_key, PublicKey)
        assert private_key.public_key == public_key

    def test_error_on_out_of_range_secret(self):
        """A secret must be in the range [1, n-1]."""
        with pytest.raises(ValueError):
            PrivateKey(secret=0, curve=curve)

        with pytest.raises(ValueError):
            PrivateKey(secret=curve.n, curve=curve)

    def test_error_on_missing_curve(self):
        """The curve is a required keyword-only argument."""
        with pytest.raises(TypeError):
            PrivateKey(secret=5)  # pyright: ignore[reportCallIssue]


# --- Property-Based Testing ---

curves = st.just(secp256k1)


@st.composite
def private_keys(draw, curve):
    """A Hypothesis strategy to generate a PrivateKey for a given curve."""
    secret = draw(st.integers(min_value=1, max_value=curve.n - 1))
    return PrivateKey(secret=secret, curve=curve)


# --- Tests ---


@given(curve=curves)
def test_generate_keypair_is_valid(curve):
    """
    Property: The keypair generated by the helper function must be valid.
    The public key must correspond to the private key's secret.
    """
    private_key, public_key = generate_keypair(curve)
    assert isinstance(private_key, PrivateKey)
    assert isinstance(public_key, PublicKey)

    assert private_key.public_key == public_key
    assert public_key.point == private_key.secret * curve.G


@given(private_key=private_keys(secp256k1))
def test_public_key_is_always_on_curve(private_key):
    """
    Property: The public key must always be a valid point on its curve.
    This is a crucial security guarantee.
    """
    public_key = private_key.public_key
    point = public_key.point
    curve = public_key.curve

    assert point.y**2 == point.x**3 + curve.a * point.x + curve.b


@given(private_key=private_keys(secp256k1))
def test_key_relationship_property(private_key):
    """
    Property: The public key must always equal secret * G.
    This is the fundamental definition of an elliptic curve key pair.
    """
    public_key = private_key.public_key
    G = private_key.curve.G
    assert public_key.point == private_key.secret * G
