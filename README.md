# ECC

[![PyPI version](https://badge.fury.io/py/eccrypto.svg)](https://pypi.org/project/eccrypto/)
[![License](https://img.shields.io/github/license/drtoxic69/ECC)](./LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/eccrypto)](https://pypi.org/project/eccrypto/)
[![Issues](https://img.shields.io/github/issues/drtoxic69/ECC)](https://github.com/drtoxic69/ECC/issues)


A pure Python library for **Elliptic Curve Cryptography (ECC)** — built from scratch with clarity and educational readability in mind.
Supports digital signatures (ECDSA), key generation, and secure field arithmetic over common curves like `secp256k1`, `P-256`, and more.

---

## ✨ Features
- Finite field arithmetic over prime fields (`FieldElement`)
- Curve definition (`Curve` and `Point`)
- ECC point addition, doubling, and scalar multiplication
- Key pair generation (`keys.py`)
- ECDSA signature generation and verification (`ecdsa.py`)
- Built-in support for popular curves (`secp256k1`, `P-256`, `brainpool`, etc.)
- Easy-to-understand documentation in every module for educational purposes

---

## 📦 Installation

### From PyPI:
```bash
pip install eccrypto
```

## 🔍 Quick Examples

### 🔑 Key Generation

```python
from ecc import generate_keypair
from ecc import secp256k1

priv, pub = generate_keypair(secp256k1)

print("Private Key:\n", priv)
print("Public Key:\n", pub)
```

### ✍️ ECDSA Sign & Verify

```python
from ecc import secp256k1
from ecc import generate_keypair
from ecc import sign, verify

priv, pub = generate_keypair(secp256k1)

msg = b"Heyy! :D"
signature = sign(msg, priv)
print("Signature:", signature)

valid = verify(msg, signature, pub)

if valid:
    print("The signtature is valid!")
```

### 📌 Curve and Point Usage

```python
from ecc import Curve, Point

a, b = 2, 2             # Curve: y^2 = x^3 + 2x + 2

P = 17                  # Prime modulus
G = (5, 1)              # Generator Point
n = 19                  # Number of points in E(Z/17Z)

curve = Curve(a, b, P, G, n)
print(curve)

G = Point(5, 1, curve)
print("Generator point: ", G)

P  = 2 * G              # Scalar Multiplication
P1 = P + P              # Point Addition

print("2G = ", P)
print("2G + 2G = ", P1)
```

### 🔢 Field Arithmetic

```python
from ecc import FieldElement

a = FieldElement(7, 13)
b = FieldElement(8, 13)

print("a + b =", a + b)
print("a * b =", a * b)
print("a ** -1 =", a ** -1)  # Inverse of a
```

---

## 🧪 Testing

You can run the test suite using pytest:

```bash
pytest
```

All tests are located in the `tests/` directory and cover field arithmetic, point operations, key generation, and ECDSA functionality.

---

## 🤝 Contributions Welcome

PRs for adding new curves, improving documentation, and optimizations are welcome. Please make sure all tests pass.

---

## 📄 License

Licensed under the GPL-3.0 License. See [LICENSE](./LICENSE).

---

## 📞 Contact

**Author:** Shivakumar
**Email:** shivakumarjagadish12@gmail.com
**GitHub:** [drtoxic69](https://github.com/drtoxic69)

For questions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/drtoxic69/ECC) or contact me directly via email.
