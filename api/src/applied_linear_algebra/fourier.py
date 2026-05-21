"""Least-squares Fourier approximation of a target function.

Given samples (x_i, y_i), find coefficients c_j minimizing

  ‖ y - (c_0 + Σ_j a_j sin((2j+1) x) + Σ_j b_j cos(j x)) ‖²

The original Project_10 fit only odd-indexed sines to a step function. We
generalize: arbitrary target callable, choose harmonic count, optionally
include cosines. Setup builds a design matrix and hands the linear least-
squares problem to ``np.linalg.lstsq``.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.floating]


@dataclass
class FourierFit:
    coefficients: FloatArray
    basis_x: FloatArray
    basis_y: FloatArray
    target_y: FloatArray
    residual_norm: float
    n_harmonics: int


def build_design(x: FloatArray, n_harmonics: int, *, include_cosines: bool) -> FloatArray:
    """Design matrix with constant + sines (+ cosines)."""
    cols: list[FloatArray] = [np.ones_like(x)]
    for j in range(n_harmonics):
        cols.append(np.sin((2 * j + 1) * x))
    if include_cosines:
        for j in range(1, n_harmonics + 1):
            cols.append(np.cos(j * x))
    return np.column_stack(cols)


def fit_fourier(
    target: Callable[[FloatArray], FloatArray] | FloatArray,
    *,
    x_eval: FloatArray | None = None,
    x_train: FloatArray | None = None,
    n_harmonics: int = 25,
    include_cosines: bool = False,
    x_range: tuple[float, float] = (-10.0, 10.0),
    n_points: int = 500,
) -> FourierFit:
    """Fit a truncated Fourier series.

    ``target`` may be a callable f(x) -> y or a precomputed y vector evaluated
    at ``x_train``. If a callable is supplied without ``x_train``, samples are
    drawn from a uniform grid on ``x_range``.
    """
    if x_eval is None:
        x_eval = np.linspace(x_range[0], x_range[1], n_points)

    if callable(target):
        if x_train is None:
            x_train = np.linspace(x_range[0], x_range[1], 200)
        y_train = np.asarray(target(x_train), dtype=np.float64)
    else:
        if x_train is None:
            raise ValueError("x_train is required when target is a precomputed array.")
        y_train = np.asarray(target, dtype=np.float64)

    A = build_design(x_train, n_harmonics, include_cosines=include_cosines)
    coef, *_ = np.linalg.lstsq(A, y_train, rcond=None)

    A_eval = build_design(x_eval, n_harmonics, include_cosines=include_cosines)
    y_pred = A_eval @ coef
    residual = float(np.linalg.norm(A @ coef - y_train))

    return FourierFit(
        coefficients=coef,
        basis_x=x_eval,
        basis_y=y_pred,
        target_y=y_train,
        residual_norm=residual,
        n_harmonics=n_harmonics,
    )


def step_function(x: FloatArray) -> FloatArray:
    """Square-wave target from the original coursework — 1 on [0, π), 0 elsewhere."""
    period = 2 * np.pi
    phase = x % period
    return np.where(phase < np.pi, 1.0, 0.0)
