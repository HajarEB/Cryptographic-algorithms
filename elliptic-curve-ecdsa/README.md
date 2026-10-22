# Elliptic Curve Cryptography & ECDSA

This project was developed as part of the **Cryptography course at Tampere University, Finland**, based on the course's programming assignments and supporting materials.

It implements elliptic curve cryptography (ECC) and the Elliptic Curve Digital Signature Algorithm (ECDSA) in Python, using custom arbitrary-precision arithmetic.

The implementation covers big-number operations, elliptic curve point arithmetic, public key generation, and randomized ECDSA signing.

## Features

### 1. Arbitrary-Precision Arithmetic (`bignum.py`)
- Big integers represented as lists of digits in an arbitrary base.
- Addition, subtraction, and multiplication.
- Modular arithmetic, division, and modular inversion using the Extended Euclidean Algorithm.
- Conversion between numerical bases.

### 2. Elliptic Curve Operations (`bignum.py`)
- Elliptic curve point addition and doubling.
- Scalar multiplication using the double-and-add algorithm.
- Elliptic curve operations performed using the big-number arithmetic functions.

### 3. ECDSA Signature Generation (`ecdsa.py`)
- ECDSA signing using the SEC2 `secp112r1` elliptic curve.
- Conversion of hexadecimal inputs into arbitrary-base big-number representations.
- Random ephemeral-key generation for signing.
- Generation of signature components `(r, s)` as hexadecimal strings.

### 4. Public Key Generation (`keygen.py`)
- Derivation of the public key from a private key using elliptic curve scalar multiplication.

## Project Structure

```text
elliptic-curve-ecdsa/
├── bignum.py        # Big-number and elliptic curve operations
├── ecdsa.py         # ECDSA signature generation
├── keygen.py        # Public key generation
└── test.py          # Basic signature generation tests
```

## Usage

Requires Python 3. No external dependencies.

Run the example test:

```bash
python test.py
```

The test generates two ECDSA signatures for the same private key and message hash, prints both signatures, and performs basic checks on their output format and nonzero values.

## Implementation Notes

- Cryptographic calculations use the custom big-number representation rather than Python's built-in arbitrary-precision integers.
- The implementation uses the 112-bit `secp112r1` curve specified in the coursework.
- The test script checks basic signature output properties; it does not perform cryptographic signature verification.
- Some supporting arithmetic routines were provided as part of the coursework and integrated with the implemented functions.

## Disclaimer

This project was developed for educational purposes as part of the Tampere University cryptography course. The 112-bit elliptic curve and the random-number generation approach are not suitable for production cryptographic applications.
