import pytest

from ecc import Curve, Point

curve = Curve(P=17, a=2, b=2, G=(5, 1), n=19, h=1, name="toy_curve")


class TestCurve:
    """Tests the functionality of the Curve class."""

    def test_init(self):
        """Test that curve parameters are initialized correctly."""
        assert curve.P == 17
        assert curve.a.num == 2
        assert curve.b.num == 2
        assert curve.name == "toy_curve"

    def test_repr(self):
        """Test the __repr__ method for a clean representation."""
        assert repr(curve) == "Curve(toy_curve)"

        # Test representation for a curve without a name
        unnamed_curve = Curve(P=17, a=2, b=2, G=(5, 1), n=19)
        assert repr(unnamed_curve) == "Curve(y² = x³ + 2x + 2 mod 17)"

    def test_eq(self):
        """Test the __eq__ method for comparing curves."""
        curve1 = Curve(P=17, a=2, b=2, G=(5, 1), n=19)
        curve2 = Curve(P=17, a=2, b=2, G=(5, 1), n=19)
        assert curve1 == curve2

        curve3 = Curve(P=19, a=2, b=2, G=(5, 1), n=19)
        assert curve1 != curve3

    def test_generator_property(self):
        """Test that the G property returns a valid Point object."""
        G = curve.G
        assert isinstance(G, Point)

        # Assertion: Type safety
        assert G.x is not None and G.y is not None

        assert G.x.num == 5 and G.y.num == 1
        assert G.curve == curve

        G2 = curve.G
        assert id(G) == id(G2)


class TestCurveErrors:
    """Tests the error handling of the Curve class."""

    def test_singular_curve(self):
        """Test that initializing a singular curve raises a ValueError."""
        # For y² = x³ - 3x + 2 over F_17, the discriminant is 0
        with pytest.raises(ValueError, match="This is a singular curve"):
            Curve(P=17, a=-3, b=2, G=(1, 0), n=19)
