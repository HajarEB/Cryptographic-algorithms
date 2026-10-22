# Cryptographic Algorithms – Python Implementations

A collection of cryptographic algorithms implemented in Python as part of the **Cryptography course at Tampere University, Finland**.

The project covers fundamental concepts in symmetric and asymmetric cryptography, including modular arithmetic, Feistel networks, substitution boxes, hash constructions, primality testing, arbitrary-precision arithmetic, elliptic curve cryptography, and digital signatures.

The implementations were developed as programming exercises to explore the mathematical foundations and internal workings of cryptographic algorithms.

## Projects

### 1. [Cryptographic Algorithms](./cryptographic-foundations/)

Implementations of fundamental mathematical operations and symmetric cryptographic constructions.

**Key features:**
- Modular exponentiation and polynomial arithmetic over finite fields.
- Probabilistic primality testing using Miller–Rabin.
- Primitive root computation and the Chinese Remainder Theorem.
- Personalized 16-round Feistel encryption network.
- AES-inspired transformations and a custom Keccak-inspired sponge construction.

**Files:** `modular_polynomial_arithmetic.py`, `number_theory.py`, `feistel_network.py`, `aes_keccak.py`

See the [project README](./cryptographic-foundations/README.md) for implementation details and usage instructions.

### 2. [Elliptic Curve Cryptography & ECDSA](./elliptic-curve-ecdsa/)

Implementation of elliptic curve operations and ECDSA digital signature generation using custom arbitrary-precision arithmetic.

**Key features:**
- Arbitrary-precision integer arithmetic and modular inversion.
- Elliptic curve point addition, doubling, and scalar multiplication.
- Public key generation using elliptic curve scalar multiplication.
- ECDSA signature generation using the `secp112r1` elliptic curve.
- Basic signature-generation tests.

**Files:** `bignum.py`, `ecdsa.py`, `keygen.py`, `test.py`

See the [project README](./elliptic-curve-ecdsa/README.md) for implementation details and usage instructions.

## Repository Structure

```text
cryptography-algorithms/
├── cryptographic-foundations/
│   ├── modular_polynomial_arithmetic.py
│   ├── feistel_network.py
│   ├── aes_keccak.py
│   ├── number_theory.py
│   └── README.md
│
├── elliptic-curve-ecdsa/
│   ├── bignum.py
│   ├── ecdsa.py
│   ├── keygen.py
│   ├── test.py
│   └── README.md
│
└── README.md
```

## Technologies

- **Language:** Python 3
- **Dependencies:** Python standard library only
- **Concepts:** Number theory, finite-field arithmetic, symmetric cryptography, elliptic curve cryptography, digital signatures

## Usage

Clone the repository:

```bash
git clone https://github.com/<username>/cryptography-algorithms.git
cd cryptography-algorithms
```

Each project can be executed independently. Refer to its README for specific commands and examples.

## Disclaimer

These implementations were developed for educational purposes. Some constructions use personalized algorithms or legacy cryptographic parameters and are **not intended for production security applications**.
