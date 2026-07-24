# Encrypt-then-MAC Cryptography Demo

## Overview

This repository contains a compact Python implementation of an authenticated encryption workflow.

The program encrypts plaintext using AES in CBC mode, then authenticates the IV and ciphertext using HMAC-SHA256. It also includes a small set of built-in tests that verify normal encryption/decryption and confirm that modified ciphertext or modified MAC values are rejected.

The aim is to demonstrate the core idea of **encrypt-then-MAC**: encrypt the message first, then authenticate the encrypted output before allowing decryption.

## Repository Contents

```text
.
├── encrypt_then_mac.py   # AES-CBC encryption, HMAC generation and test cases
├── requirements.txt      # Python dependencies
├── LICENSE.txt           # Usage terms
└── README.md             # Project documentation
```

## What the Program Demonstrates

- Symmetric encryption with AES.
- CBC mode encryption using a random IV.
- PKCS7 padding for block alignment.
- HMAC-SHA256 message authentication.
- Encrypt-then-MAC ordering.
- Verification before decryption.
- Simple tamper-detection tests.

## Technical Summary

The implementation is built around four main functions:

| Function | Purpose |
|---|---|
| `aes_encrypt()` | Encrypts UTF-8 plaintext using AES-CBC with PKCS7 padding. |
| `generate_hmac()` | Generates a SHA-256 HMAC over supplied data. |
| `encrypt_then_mac()` | Encrypts plaintext, then authenticates `IV + ciphertext`. |
| `decrypt_and_verify()` | Recomputes the MAC, verifies integrity, then decrypts. |

## Security Design

The program uses an encrypt-then-MAC construction:

```text
plaintext -> AES-CBC encryption -> IV + ciphertext -> HMAC-SHA256
```

During decryption, the MAC is checked before the ciphertext is decrypted:

```text
received IV + ciphertext + MAC -> verify MAC -> decrypt only if valid
```

This is important because it prevents the program from processing tampered ciphertext. If the ciphertext or MAC is modified, verification fails and the function raises a `ValueError`.

## Dependencies

The code uses the Python `cryptography` package.

Install it with:

```bash
pip install cryptography
```

The script also uses Python's built-in `os` module for random key and IV generation.

## How to Run

Clone or download the repository, then run:

```bash
python cryptography.py
```

Expected output:

```text
Basic functionality test passed
Empty plaintext test passed
Long plaintext test passed
Modified ciphertext test passed
Modified MAC test passed
```

## Built-in Tests

The file includes five direct test cases:

| Test | What it checks |
|---|---|
| Basic functionality | A normal plaintext encrypts and decrypts correctly. |
| Empty plaintext | An empty string is handled correctly. |
| Long plaintext | A large plaintext can be encrypted and decrypted. |
| Modified ciphertext | Tampering with ciphertext causes verification failure. |
| Modified MAC | Tampering with the MAC causes verification failure. |

These tests are placed under repeated `if __name__ == "__main__":` blocks, so they run sequentially when the script is executed directly.

## Example Usage

```python
import os
from cryptography import encrypt_then_mac, decrypt_and_verify

aes_key = os.urandom(32)
mac_key = os.urandom(32)

plaintext = "Confidential message"
iv, ciphertext, mac = encrypt_then_mac(plaintext, aes_key, mac_key)

decrypted = decrypt_and_verify(iv, ciphertext, mac, aes_key, mac_key)
print(decrypted)
```

## Key Material

The example generates separate 256-bit keys for encryption and authentication:

```python
aes_key = os.urandom(32)
mac_key = os.urandom(32)
```

Using separate keys for AES and HMAC is good practice because encryption and authentication should not reuse the same key material.

## Limitations

- This is a learning/demo implementation rather than a production-ready encryption library.
- The script does not include persistent key storage or key management.
- The MAC comparison uses direct equality rather than a constant-time verification method.
- AES-CBC is used for educational purposes; modern systems commonly use AEAD modes such as AES-GCM or ChaCha20-Poly1305.
- The tests are basic script-level checks rather than a structured `pytest` test suite.

## Skills Demonstrated

- Python cryptography implementation.
- Symmetric encryption concepts.
- Message authentication.
- Secure ordering of encryption and integrity checks.
- Tamper-detection testing.
- Basic defensive programming with explicit failure on invalid MACs.

## Notes

This project focuses on demonstrating the mechanics of authenticated encryption. It shows why confidentiality alone is not enough: encrypted data also needs integrity protection so that modified ciphertext is detected before decryption occurs.

## Usage Notice

This repository is provided for portfolio and review purposes only.

All rights are reserved. No permission is granted to copy, redistribute, submit, or reuse this work, in whole or in part, for academic coursework, assessment, or commercial purposes.
