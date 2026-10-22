# Cryptographic Algorithms – Python Implementations

A collection of cryptographic algorithms implemented in Python as part of the **Cryptography course at Tampere University, Finland**.

The project covers fundamental concepts in symmetric and asymmetric cryptography, including modular arithmetic, Feistel networks, substitution boxes, hash constructions, primality testing, arbitrary-precision arithmetic, elliptic curve cryptography, and digital signatures.

The implementations were developed as programming exercises to explore the mathematical foundations and internal workings of cryptographic algorithms.

## Projects

### 1. [Cryptographic Foundations](./cryptographic-foundations/)

Number theory and symmetric constructions built from first principles.

- Finite-field polynomial arithmetic, Miller–Rabin primality testing, primitive roots, and CRT.
- A 16-round Feistel network and an AES/Keccak-inspired sponge hash.

See the [project README](./cryptographic-foundations/README.md) for implementation details and usage instructions.

### 2. [Elliptic Curve Cryptography & ECDSA](./elliptic-curve-ecdsa/)

ECDSA on the `secp112r1` curve, built on a custom arbitrary-precision integer library.

- Big-number arithmetic and elliptic curve point operations, implemented without Python's built-in big integers.
- Key generation, signing, and verification, tested with sign→verify round-trips.

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
