"""Tests for the Hill cipher (modular)."""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from applied_linear_algebra import hill_cipher


def test_encrypt_decrypt_round_trip_simple() -> None:
    A = np.array([[1, 2], [3, 5]], dtype=np.int64)
    b = np.array([7, 11], dtype=np.int64)
    plaintext = "hello world"
    ciphertext = hill_cipher.encrypt(plaintext, A, b)
    decrypted = hill_cipher.decrypt(ciphertext, A, b)
    assert decrypted.rstrip() == plaintext.rstrip()


def test_mod_inverse_basic() -> None:
    assert (3 * hill_cipher.mod_inverse(3, 7)) % 7 == 1
    assert (5 * hill_cipher.mod_inverse(5, 101)) % 101 == 1


def test_mod_inverse_rejects_non_invertible() -> None:
    with pytest.raises(ValueError):
        hill_cipher.mod_inverse(0, 7)


def test_matrix_mod_inverse_round_trip() -> None:
    p = 101
    A = np.array([[2, 3], [5, 7]], dtype=np.int64)
    A_inv = hill_cipher.matrix_mod_inverse(A, p)
    product = (A @ A_inv) % p
    np.testing.assert_array_equal(product, np.eye(2, dtype=np.int64))


def test_matrix_mod_inverse_rejects_singular() -> None:
    A = np.array([[2, 4], [1, 2]], dtype=np.int64)  # rank 1
    with pytest.raises(ValueError):
        hill_cipher.matrix_mod_inverse(A, 101)


def test_random_key_generates_invertible_matrix() -> None:
    A, b = hill_cipher.random_key(block_size=3, seed=0)
    inv = hill_cipher.matrix_mod_inverse(A, hill_cipher.MODULUS)
    np.testing.assert_array_equal(
        (A @ inv) % hill_cipher.MODULUS, np.eye(3, dtype=np.int64)
    )


@given(
    # Exclude alphabet[0] ('a') so trailing-zero strip doesn't eat real chars.
    text=st.text(
        alphabet=list("bcdefghijklmnopqrstuvwxyz "),
        min_size=1,
        max_size=80,
    ),
    block_size=st.integers(min_value=2, max_value=4),
    seed=st.integers(min_value=0, max_value=10),
)
@settings(max_examples=20, deadline=None)
def test_round_trip_property(text: str, block_size: int, seed: int) -> None:
    """Any text not ending in alphabet[0] round-trips exactly."""
    A, b = hill_cipher.random_key(block_size, seed=seed)
    ciphertext = hill_cipher.encrypt(text, A, b)
    decrypted = hill_cipher.decrypt(ciphertext, A, b)
    assert decrypted == text
