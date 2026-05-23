"""Tests for the linearized Lotka-Volterra simulation."""

from __future__ import annotations

import numpy as np
import pytest

from applied_linear_algebra import lotka_volterra


def test_trajectory_shape() -> None:
    A = [[1.9, -8.0], [0.1, 0.1]]
    result = lotka_volterra.simulate(A, x0=[100.0, 12.0], horizon=10)
    assert result.trajectory.shape == (11, 2)


def test_identity_dynamics_preserves_state() -> None:
    A = np.eye(2)
    result = lotka_volterra.simulate(A, x0=[5.0, 3.0], horizon=20)
    np.testing.assert_array_equal(result.trajectory, np.tile([5.0, 3.0], (21, 1)))


def test_intervention_offset_applied_each_step() -> None:
    A = np.zeros((2, 2))
    result = lotka_volterra.simulate(
        A, x0=[10.0, 10.0], horizon=3, intervention=[-1.0, 1.0]
    )
    assert result.trajectory[0].tolist() == [10.0, 10.0]
    assert result.trajectory[1].tolist() == [-1.0, 1.0]
    assert result.trajectory[2].tolist() == [-1.0, 1.0]


def test_rejects_non_2x2_A() -> None:
    with pytest.raises(ValueError):
        lotka_volterra.simulate(np.eye(3), x0=[1.0, 1.0])


def test_rejects_bad_x0() -> None:
    with pytest.raises(ValueError):
        lotka_volterra.simulate(np.eye(2), x0=[1.0, 2.0, 3.0])


def test_eigenvalues_complex_for_oscillating_dynamics() -> None:
    """The default predator-prey matrix should have complex eigenvalues."""
    result = lotka_volterra.simulate(
        [[1.9, -8.0], [0.1, 0.1]], x0=[100.0, 12.0], horizon=20
    )
    assert any(abs(z.imag) > 1e-6 for z in result.eigenvalues)


def test_extinction_flagged() -> None:
    """Negative initial state propagates to extinction immediately."""
    A = np.eye(2)
    result = lotka_volterra.simulate(A, x0=[10.0, 10.0], horizon=5, intervention=[-100.0, 0.0])
    assert result.extinct
    assert result.extinction_time == 1
