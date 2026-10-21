# Cryptographic Algorithms – Python Implementations

A collection of cryptographic algorithms implemented in Python as part of the **Cryptography course at Tampere University**.

The project covers fundamental techniques used in symmetric and asymmetric cryptography, including modular arithmetic, Feistel networks, substitution boxes, hash constructions, primality testing, arbitrary-precision arithmetic, elliptic curve cryptography, and digital signatures.

The implementations were developed as programming exercises to explore the mathematical foundations and internal workings of cryptographic algorithms.

## Implemented Algorithms

| File | Algorithms and Concepts |
|---|---|
| `modular_polynomial_arithmetic.py` | Square-and-multiply, Extended Euclidean Algorithm, modular polynomial arithmetic |
| `feistel_network.py` | Feistel network construction and encryption with round keys |
| `aes_keccak.py` | Personalized S-box generation, sponge construction, AES-inspired transformations |
| `number_theory.py` | Miller–Rabin primality testing, primitive roots, Chinese Remainder Theorem |
| `bignum.py` | Arbitrary-precision arithmetic, division, modular reduction, modular inversion |
| `elliptic_curve.py` | Elliptic curve point addition, doubling, scalar multiplication |
| `ecdsa.py` | Elliptic Curve Digital Signature Algorithm (ECDSA) |

## 1. Modular and Polynomial Arithmetic

**File:** `modular_polynomial_arithmetic.py`  
**Exercises:** P1–P2

Implements fundamental arithmetic algorithms used in cryptography.

- Square-and-multiply for efficient modular exponentiation.
- Extended Euclidean Algorithm for computing greatest common divisors and Bézout coefficients.
- Polynomial arithmetic over finite fields.
- Polynomial division and remainder computation modulo a prime.

These operations provide the mathematical foundation for more advanced public-key cryptographic algorithms.

## 2. Feistel Network

**File:** `feistel_network.py`  
**Exercises:** P3–P4

Implements a custom Feistel-based encryption scheme to demonstrate the principles behind Feistel block ciphers.

- Block processing using left and right halves.
- Multiple rounds of Feistel transformations.
- Round-dependent transformations.
- Key schedule generation using matrix operations.
- Encryption using round keys and modular arithmetic.

The implementation demonstrates how repeated transformations and key-dependent operations can be combined to construct a block cipher.

## 3. AES-Inspired Sponge Construction

**File:** `aes_keccak.py`  
**Exercises:** P5–P7

Implements a custom hash-like construction combining AES-inspired transformations with sponge-based processing.

### Personalized S-box

- Generation of a 256-element substitution permutation.
- Permutation cycle analysis.
- Fixed-point detection and modification.

### Sponge Construction

- Block-based input absorption.
- Internal state transformations.
- Output generation through squeezing.

### AES-Inspired Transformations

- **SubBytes:** Byte substitution using the personalized S-box.
- **ShiftRows:** Row-wise cyclic rotations.
- **MixColumns:** Matrix-based state mixing using modular arithmetic.
- Repeated transformation rounds during absorption and squeezing.

This is an educational AES-inspired sponge construction, not an implementation of standard AES or Keccak.

## 4. Number Theory

**File:** `number_theory.py`  
**Exercises:** P8–P9

Implements number-theoretic algorithms commonly used in public-key cryptography.

- Prime candidate generation using small-prime sieving.
- Miller–Rabin probabilistic primality testing.
- Primitive root calculation modulo a prime.
- Chinese Remainder Theorem (CRT).
- Modular arithmetic operations.

These algorithms illustrate mathematical techniques used in cryptographic key generation and RSA-related computations.

## 5. Arbitrary-Precision Arithmetic

**File:** `bignum.py`  
**Exercise:** P10

Implements arithmetic operations on arbitrarily large non-negative integers represented as lists of digits in a configurable base.

- Base conversion and normalization.
- Comparison, addition, subtraction, and multiplication.
- Integer division and remainder.
- Modular reduction and subtraction.
- Extended Euclidean Algorithm for large integers.
- Modular multiplicative inversion.

The implementation explores how arithmetic with large integers can be performed using custom data structures rather than relying directly on Python's built-in arbitrary-precision integer operations.

## 6. Elliptic Curve Arithmetic

**File:** `elliptic_curve.py`  
**Exercises:** P11–P12

Implements fundamental elliptic curve operations over prime fields.

- Elliptic curve point addition.
- Point doubling.
- Handling the point at infinity.
- Scalar multiplication using the double-and-add algorithm.
- Elliptic curve operations using custom arbitrary-precision arithmetic.

These operations form the mathematical foundation of elliptic curve cryptographic schemes.

## 7. ECDSA Digital Signatures

**File:** `ecdsa.py`  
**Exercise:** P13

Implements the signing operation of the **Elliptic Curve Digital Signature Algorithm (ECDSA)** using custom arbitrary-precision arithmetic.

- Elliptic curve public-key derivation.
- Ephemeral scalar generation.
- Elliptic curve scalar multiplication.
- Modular inversion.
- Signature generation as a pair of hexadecimal values.

The implementation uses the 112-bit `secp112r1` elliptic curve parameters from SEC 2 and builds on the arithmetic developed in earlier exercises.

## Technologies and Concepts

**Language:** Python

**Cryptographic concepts:**
- Symmetric encryption
- Cryptographic hash constructions
- Modular arithmetic and finite fields
- Number theory and primality testing
- Arbitrary-precision arithmetic
- Elliptic curve cryptography
- Digital signatures

## Educational Purpose

These implementations were developed for educational purposes to understand cryptographic algorithms at a mathematical and implementation level.

They are not intended for production use or for protecting sensitive information. In particular, the custom cipher and hash constructions are not standardized cryptographic primitives, and the ECDSA exercise uses a legacy 112-bit curve that does not meet modern security requirements.

## Acknowledgments

Developed as part of the Cryptography coursework at **Tampere University, Finland**.

The exercise specifications and algorithmic requirements were provided by the course. The Python programming implementations were completed independently.
