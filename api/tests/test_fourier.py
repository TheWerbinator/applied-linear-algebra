"""Tests for the Fourier least-squares fit."""

from __future__ import annotations

import numpy as np

from applied_linear_algebra import fourier


def test_fit_sine_recovers_first_coefficient() -> None:
    """A pure sine target should be reconstructed with negligible residual."""
    x = np.linspace(-np.pi, np.pi, 400)
    y = np.sin(x)
    fit = fourier.fit_fourier(
        y,
        x_train=x,
        x_eval=x,
        n_harmonics=5,
    )
    assert fit.residual_norm < 1e-8
    np.testing.assert_allclose(fit.basis_y, y, atol=1e-6)


def test_step_function_takes_values_in_zero_one() -> None:
    x = np.linspace(-10, 10, 1000)
    y = fourier.step_function(x)
    assert set(np.unique(y).tolist()) == {0.0, 1.0}


def test_increasing_harmonics_decreases_residual() -> None:
    x = np.linspace(-3 * np.pi, 3 * np.pi, 500)
    target_y = fourier.step_function(x)
    coarse = fourier.fit_fourier(target_y, x_train=x, x_eval=x, n_harmonics=3)
    fine = fourier.fit_fourier(target_y, x_train=x, x_eval=x, n_harmonics=25)
    assert fine.residual_norm < coarse.residual_norm


def test_design_matrix_shape_no_cosines() -> None:
    x = np.linspace(0, 1, 10)
    A = fourier.build_design(x, n_harmonics=5, include_cosines=False)
    assert A.shape == (10, 6)  # 1 constant + 5 sines


def test_design_matrix_shape_with_cosines() -> None:
    x = np.linspace(0, 1, 10)
    A = fourier.build_design(x, n_harmonics=5, include_cosines=True)
    assert A.shape == (10, 11)  # 1 constant + 5 sines + 5 cosines
