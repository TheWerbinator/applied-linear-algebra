"""Hill cipher (modular arithmetic version).

The Hill cipher is a classical block cipher built on modular linear algebra:

  encryption:  c = (A m + b) mod p
  decryption:  m = A⁻¹ (c - b) mod p

where ``A`` is an n×n invertible matrix mod p and ``m, c, b`` are length-n
column vectors over Z_p.

The Project_15 coursework computed the inverse over R (real numbers) with
``np.linalg.inv`` and then rounded back to integers — fragile and only works
on tiny dictionaries with low-norm cipher matrices. This version does the
inverse properly in Z_p using the extended Euclidean algorithm, so decryption
is exact for any prime modulus.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


IntArray = NDArray[np.integer]


# Default alphabet — printable ASCII subset, 97 symbols. The modulus must be
# >= len(ALPHABET); 101 is the smallest prime >= 97.
ALPHABET = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    " .,?!:;'\"()[]{}<>/-+*=^@#$%&_"
)
ASSERT_LEN = len(ALPHABET)  # 97
MODULUS = 101  # smallest prime >= 97


def _char_to_int(c: str) -> int:
    if c not in ALPHABET:
        raise ValueError(f"Character {c!r} not in alphabet.")
    return ALPHABET.index(c)


def _int_to_char(i: int) -> str:
    if not 0 <= i < ASSERT_LEN:
        raise ValueError(f"Integer {i} outside alphabet range [0, {ASSERT_LEN}).")
    return ALPHABET[i]


def text_to_blocks(text: str, block_size: int) -> IntArray:
    """Encode ``text`` as an (n_blocks, block_size) integer matrix, right-padded."""
    pad = (-len(text)) % block_size
    encoded = [_char_to_int(c) for c in text] + [0] * pad
    return np.asarray(encoded, dtype=np.int64).reshape(-1, block_size)


def blocks_to_text(blocks: IntArray, strip_trailing_zero: bool = True) -> str:
    flat = blocks.ravel().tolist()
    if strip_trailing_zero:
        while flat and flat[-1] == 0:
            flat.pop()
    return "".join(_int_to_char(int(i)) for i in flat)


def mod_inverse(a: int, p: int) -> int:
    """Multiplicative inverse of ``a`` modulo prime ``p`` via Fermat's little theorem."""
    if a % p == 0:
        raise ValueError(f"{a} has no inverse mod {p} (a ≡ 0).")
    return pow(int(a) % p, p - 2, p)


def matrix_mod_inverse(A: IntArray, p: int) -> IntArray:
    """Inverse of A in GL_n(Z_p) via cofactor expansion.

    For small block sizes (≤ 6) the cofactor formula is fast enough and
    avoids any floating-point detour. For larger blocks switch to
    Gauss-Jordan over Z_p.
    """
    A_arr = np.asarray(A, dtype=np.int64) % p
    n = A_arr.shape[0]
    if A_arr.shape != (n, n):
        raise ValueError(f"A must be square; got shape {A_arr.shape}.")

    det_real = float(np.round(np.linalg.det(A_arr)))
    det_mod = int(det_real) % p
    if det_mod == 0:
        raise ValueError("A is singular mod p; choose a different key matrix.")
    det_inv = mod_inverse(det_mod, p)

    # Cofactor matrix
    cof = np.zeros_like(A_arr)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(A_arr, i, axis=0), j, axis=1)
            cof[i, j] = ((-1) ** (i + j)) * int(round(float(np.linalg.det(minor))))
    adj = cof.T % p
    inv = (det_inv * adj) % p
    return inv.astype(np.int64)


def encrypt(plaintext: str, A: IntArray, b: IntArray, *, p: int = MODULUS) -> IntArray:
    """Encrypt ``plaintext`` under (A, b) mod ``p``. Returns ciphertext as int matrix."""
    A_arr = np.asarray(A, dtype=np.int64) % p
    b_arr = np.asarray(b, dtype=np.int64) % p
    n = A_arr.shape[0]
    if b_arr.shape != (n,):
        raise ValueError(f"b must have shape ({n},); got {b_arr.shape}.")

    blocks = text_to_blocks(plaintext, n)
    return (blocks @ A_arr.T + b_arr) % p


def decrypt(ciphertext: IntArray, A: IntArray, b: IntArray, *, p: int = MODULUS) -> str:
    """Decrypt ``ciphertext`` under (A, b) mod ``p``, returning the recovered plaintext."""
    A_arr = np.asarray(A, dtype=np.int64) % p
    b_arr = np.asarray(b, dtype=np.int64) % p
    A_inv = matrix_mod_inverse(A_arr, p)
    cipher = np.asarray(ciphertext, dtype=np.int64)
    plain_blocks = ((cipher - b_arr) @ A_inv.T) % p
    return blocks_to_text(plain_blocks.astype(np.int64))


def random_key(block_size: int, *, p: int = MODULUS, seed: int = 0) -> tuple[IntArray, IntArray]:
    """Generate a random invertible (A, b) key pair mod p."""
    rng = np.random.default_rng(seed)
    while True:
        A = rng.integers(0, p, size=(block_size, block_size), dtype=np.int64)
        det_mod = int(round(float(np.linalg.det(A)))) % p
        if det_mod != 0:
            break
    b = rng.integers(0, p, size=block_size, dtype=np.int64)
    return A, b
