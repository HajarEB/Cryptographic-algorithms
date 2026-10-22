# Cryptographic Algorithms – Python Implementations

A collection of cryptographic algorithms implemented in Python as part of the **Cryptography course at Tampere University, Finland, 2024**.

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

- **Language:** Python 3.13
- **Dependencies:** Python standard library only
- **Concepts:** Number theory, finite-field arithmetic, symmetric cryptography, elliptic curve cryptography, digital signatures

## Usage

Clone the repository:

```bash
git clone https://github.com/HajarEB/cryptography-algorithms.git
cd cryptography-algorithms
```

Each project can be executed independently. Refer to its README for specific commands and examples.

## What I Learned / Challenges

### 1. Cryptographic Foundations

The main challenges were implementing polynomial arithmetic over finite fields and building working encryption and hashing pipelines from individual transformations. Analyzing the cycle structure of the S-box showed how a substitution mapping can be studied as a permutation. The Feistel network and the AES/Keccak-inspired sponge both required precise tracking of round states and byte representations across many transformations.

### 2. Elliptic Curve Cryptography & ECDSA

The main challenge was implementing elliptic curve operations on integers stored as digit arrays rather than Python’s built-in integers. Modular inversion, point doubling, and scalar multiplication all depended on the custom big-number arithmetic library, with values converted between numerical bases along the way. Building ECDSA on top of these layers showed how the correctness of ECDSA depends on the underlying arithmetic.

## Disclaimer

These implementations were developed for educational purposes. Some constructions use personalized algorithms or legacy cryptographic parameters and are **not intended for production security applications**.
