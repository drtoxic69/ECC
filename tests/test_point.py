import pytest
from hypothesis import given, strategies as st

from ecc import Point, Curve
from ecc import secp256k1

# --- Test Setup ---
P = 17
A = 2
B = 2
N = 19
Gx, Gy = (5, 1)

# A global curve object for our tests
curve = Curve(P=P, a=A, b=B, G=(Gx, Gy), n=N)
G = Point(Gx, Gy, curve)
I = Point(None, None, curve)


# --- Testing for Expected Errors ---
class TestPointErrors:
    def test_init_point_not_on_curve(self):
        """Points not satisfying the curve equation should raise a ValueError."""
        with pytest.raises(ValueError, match="is not on the curve"):
            Point(x=3, y=7, curve=curve)

    def test_add_points_on_different_curves(self):
        """Adding points from different curves should raise a TypeError."""
        p1 = G
        p2 = Point(secp256k1.G[0], secp256k1.G[1], secp256k1)
        with pytest.raises(TypeError, match="Points are not on the same curve"):
            p1 + p2

    def test_rmul_by_non_integer(self):
        """Scalar multiplication requires an integer scalar."""
        with pytest.raises(TypeError, match="Scalar must be an integer"):
            p = 2.5 * G


# --- Testing Edge Cases and Core Operations ---
class TestPointOperations:
    def test_addition(self):
        """Test standard point addition P + Q = R."""
        p1 = G
        p2 = Point(6, 3, curve)
        assert p1 + p2 == Point(10, 6, curve)

    def test_doubling(self):
        """Test point doubling P + P = 2P."""
        assert G + G == Point(6, 3, curve)

    def test_identity_element(self):
        """Test that adding the point at infinity is an identity operation."""
        assert G + I == G
        assert I + G == G

    def test_additive_inverse(self):
        """Test that adding a point to its inverse results in infinity."""
        p_inv = Point(G.x.num, -G.y.num, curve)
        assert G + p_inv == I


# --- Property-Based Testing (with Hypothesis) ---
integers = st.integers(min_value=1, max_value=N - 1)
points = st.integers(min_value=1, max_value=N - 1).map(lambda k: k * G)


@given(P=points)
def test_identity_property(P):
    """Property: P + O = P (where O is the identity/infinity point)."""
    assert P + I == P
    assert I + P == P


@given(P=points)
def test_inverse_property(P):
    """Property: P + (-P) = O."""
    if P.y is not None:
        P_inv = Point(P.x.num, -P.y.num, curve)
        assert P + P_inv == I


@given(k=integers, l=integers)
def test_scalar_distributivity(k, l):
    """Property: (k + l) * P = k*P + l*P."""
    p1 = (k + l) * G
    p2 = (k * G) + (l * G)
    assert p1 == p2


@given(k=integers, l=integers)
def test_scalar_associativity(k, l):
    """Property: k * (l * P) = (k * l) * P."""
    p1 = k * (l * G)
    p2 = ((k * l) % N) * G  # modulo N
    assert p1 == p2


@given(P=points, Q=points, R=points)
def test_associativity_of_addition(P, Q, R):
    """Property: (P + Q) + R = P + (Q + R)."""
    p1 = (P + Q) + R
    p2 = P + (Q + R)
    assert p1 == p2
