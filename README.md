# eccrypto: Elliptic Curve Cryptography from Scratch

[![PyPI version](https://img.shields.io/pypi/v/eccrypto.svg)](https://pypi.org/project/eccrypto/)
[![Downloads](https://static.pepy.tech/badge/eccrypto)](https://pepy.tech/project/eccrypto)
[![GitHub license](https://img.shields.io/github/license/drtoxic69/ECC)](https://github.com/drtoxic69/ECC/blob/main/LICENSE)
[![Code Quality](https://github.com/drtoxic69/ECC/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/drtoxic69/ECC/actions/workflows/code-quality.yaml)


A pure Python library for **Elliptic Curve Cryptography (ECC)**, built from scratch with a focus on security, clarity, and modern Python practices.

This library provides the essential cryptographic primitives for digital signatures and key exchange, implemented with secure, constant-time algorithms and a clean, object-oriented API. It's an excellent tool for learning the fundamentals of ECC or for projects that require a clear and auditable cryptographic implementation.

---

## ✨ Features

* **Secure by Default**:
    * **Constant-Time** scalar multiplication (Montgomery Ladder) to prevent timing side-channel attacks.
    * **Deterministic Signatures (RFC 6979)** to eliminate risks from faulty random number generators.
    * **Non-Malleable Signatures** ("low-s" normalization) to prevent signature tampering.
* **Modern API**: A clean, object-oriented interface for key management, signing, and verification.
* **Key Exchange**: Built-in support for **Elliptic Curve Diffie-Hellman (ECDH)** key exchange with a standard HKDF.
* **Core Primitives**: Includes all necessary building blocks, such as `FieldElement` and `Point` arithmetic.
* **Standard Curves**: Comes with built-in support for the `secp256k1` curve.

---

## 📦 Installation

Install the library from PyPI using `uv`:
```bash
uv add eccrypto
```
or by using `pip`:
```bash
pip install eccrypto
```

---

## 🚀 Quick Start

Here are some examples of how to use the library for common cryptographic tasks.

### 🔑 Key Generation
First, import the `secp256k1` curve and the `generate_keypair` helper function.

```python
from ecc import secp256k1
from ecc import generate_keypair

# Generate a new private and public key pair
private_key, public_key = generate_keypair(secp256k1)

print("Private Key:", private_key)
print("Public Key:", public_key)
```

### ✍️ ECDSA Signing & Verification
Use the key pair to create and verify a digital signature.

```python
# Assume `private_key` and `public_key` from the step above
message = b":D"

# Alice signs the message with her private key
signature = private_key.sign(message)
print(f"Signature: {signature}")

# Bob verifies the signature with Alice's public key
is_valid = public_key.verify(message, signature)

if is_valid:
    print("✅ Signature is valid!")
else:
    print("❌ Signature is invalid!")
```

### 🤝 ECDH Key Exchange
Establish a shared secret between two parties (Alice and Bob).

```python
# Alice and Bob both generate their own key pairs
alice_priv, alice_pub = generate_keypair(secp256k1)
bob_priv, bob_pub = generate_keypair(secp256k1)

# Alice computes the secret using her private key and Bob's public key
secret_by_alice = alice_priv.ecdh(bob_pub)

# Bob computes the secret using his private key and Alice's public key
secret_by_bob = bob_priv.ecdh(alice_pub)

# The secrets must be identical
assert secret_by_alice == secret_by_bob
print(f"\n✅ Shared secret derived successfully: 0x{secret_by_alice.hex()}")
```

---

## 📚 Documentation

For a deeper dive into the mathematical concepts behind finite fields, elliptic curve group theory, and the discriminant, please see our detailed documentation:

* [**Mathematical Foundations**](./ecc/README.md)

---

## 🛠️ Development & Testing

To set up the project for development, clone the repository and install the test dependencies:

```bash
# clone the repo
git clone git@github.com:drtoxic/ECC.git
cd ECC

# source the venv
source .venv/bin/activate

# sync
uv sync
```
---

## 🤝 Contributions

Contributions, issues, and feature requests are welcome. Please feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the GPL-3.0 License. See [LICENSE](./LICENSE).

---

## 📞 Contact

**Author:** Shivakumar
**Email:** shivakumarjagadish12@gmail.com
**GitHub:** [drtoxic69](https://github.com/drtoxic69)

For questions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/drtoxic69/ECC) or contact me directly via email.
