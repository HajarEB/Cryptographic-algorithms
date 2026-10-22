# Cryptographic Foundations

A collection of cryptographic algorithms implemented in Python, covering modular and polynomial arithmetic, Feistel-based encryption, and a custom AES-Keccak sponge construction.

Developed as part of the **Cryptography course at Tampere University, Finland**, with a focus on understanding and implementing the mathematical foundations and internal mechanisms of cryptographic systems.

## Features

### 1. Modular and Polynomial Arithmetic (`modular_polynomial_arithmetic.py`)

- Modular exponentiation using the square-and-multiply algorithm.
- Extended Euclidean Algorithm for modular arithmetic.
- Polynomial addition, subtraction, multiplication, and reduction over finite fields.
- Personalized polynomial generation and coefficient-product computation.

### 2. Feistel Network (`feistel_network.py`)

- Personalized 16-round Feistel-like encryption.
- Round-key generation using matrix multiplication.
- Block-based encryption with intermediate round-state visualization.

### 3. AES-Keccak Sponge Construction (`aes_keccak.py`)

- Personalized S-box generation and permutation-cycle analysis.
- AES-inspired transformations: SubBytes, ShiftRows, and MixColumns.
- Sponge-based file processing with six-round permutations.
- Variable-length hexadecimal digest generation.

### 4. Number Theory (`number_theory.py`)

- Probabilistic primality testing using the Miller–Rabin algorithm.
- Prime-number search using small-prime sieving.
- Primitive root computation modulo a prime.
- Chinese Remainder Theorem for solving systems of modular congruences.
  
## Project Structure

```text
cryptographic-foundations/
├── modular_polynomial_arithmetic.py
├── feistel_network.py
├── aes_keccak.py
├── number_theory.py
└── README.md
```

## Requirements

- Python 3
- No external dependencies (Python standard library only)

## Usage

Clone the repository:

```bash
git clone https://github.com/HajarEB/cryptographic-foundations.git
cd cryptographic-algorithms
```

### Modular and Polynomial Arithmetic

```bash
python modular_polynomial_arithmetic.py
```

Performs polynomial arithmetic using configurable parameters and displays the resulting polynomial remainder and coefficient product.

### Feistel Network

```bash
python feistel_network.py
```

Encrypts a predefined plaintext using a personalized 16-round encryption network and displays intermediate round states and the final ciphertext.

### AES-Keccak Sponge Construction

```bash
python aes_keccak.py
```

Prompts for an input file and the desired digest length in bytes, then processes the file and outputs a hexadecimal digest.

### Number Theory

```bash
python number_theory.py
```

Performs probabilistic prime-number search using Miller–Rabin, computes a primitive root modulo a prime, and solves a system of modular congruences using the Chinese Remainder Theorem (CRT).

The program uses predefined example parameters and displays the results of each computation.

## Disclaimer

These implementations are intended for educational and experimental purposes. The personalized Feistel network and AES-Keccak construction are not standardized cryptographic algorithms and should not be used for production security.
