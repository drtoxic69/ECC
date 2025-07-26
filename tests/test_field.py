import pytest
from hypothesis import given, strategies as st

from ecc import FieldElement


# --- Testing for Expected Errors ---
class TestFieldElementErrors:
    def test_init_invalid_prime(self):
        with pytest.raises(ValueError, match="Prime must be greater than 1."):
            FieldElement(3, 1)

    def test_init_invalid_type(self):
        with pytest.raises(TypeError, match="Number and prime must be integers."):
            FieldElement(3.5, 13)

    def test_add_mismatched_fields(self):
        a = FieldElement(7, 13)
        b = FieldElement(5, 17)
        with pytest.raises(
            TypeError, match="Cannot operate on FieldElements from different fields."
        ):
            c = a + b

    def test_division_by_zero(self):
        a = FieldElement(7, 13)
        b = FieldElement(0, 13)
        with pytest.raises((ValueError, ZeroDivisionError)):
            c = a / b


# --- Testing Edge Cases and Reflected Operations ---
class TestFieldElementOperations:
    def test_addition(self):
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        assert a + b == FieldElement(6, 13)

    def test_reflected_addition(self):
        a = FieldElement(7, 13)
        assert 5 + a == FieldElement(12, 13)

    def test_subtraction(self):
        a = FieldElement(7, 13)
        b = FieldElement(12, 13)
        assert b - a == FieldElement(5, 13)

    def test_negation(self):
        a = FieldElement(7, 13)
        assert -a == FieldElement(6, 13)
        assert a + (-a) == FieldElement(0, 13)

    def test_multiplication_by_zero(self):
        a = FieldElement(7, 13)
        zero = FieldElement(0, 13)
        assert a * zero == zero

    def test_exponentiation_to_zero(self):
        a = FieldElement(7, 13)
        identity = FieldElement(1, 13)
        assert a**0 == identity


# --- Property-Based Testing (Advanced) ---
field_elements = st.builds(FieldElement, num=st.integers(0, 12), prime=st.just(13))


@given(a=field_elements, b=field_elements)
def test_commutative_property_of_addition(a, b):
    assert a + b == b + a


@given(a=field_elements, b=field_elements)
def test_commutative_property_of_multiplication(a, b):
    assert a * b == b * a


@given(a=field_elements)
def test_multiplicative_inverse(a):
    if a.num == 0:
        return

    identity = FieldElement(1, a.prime)
    inverse = 1 / a
    assert a * inverse == identity
