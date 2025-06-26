from ecc import FieldElement


def test_addition():
    a = FieldElement(7, 13)
    b = FieldElement(12, 13)
    assert a + b == FieldElement(6, 13)


def test_exponentiation():
    a = FieldElement(3, 13)
    assert a ** 12 == FieldElement(1, 13)


def test_multiplication():
    a = FieldElement(7, 13)
    b = FieldElement(12, 13)
    assert a * b == FieldElement(6, 13)


def test_subtraction():
    a = FieldElement(7, 13)
    b = FieldElement(12, 13)
    assert b - a == FieldElement(5, 13)


def test_scalar_multiplication():
    a = FieldElement(7, 13)
    k = 2
    assert k * a == FieldElement(1, 13)


def test_division():
    a = FieldElement(7, 13)
    b = FieldElement(3, 13)
    assert a / b == FieldElement(11, 13)
