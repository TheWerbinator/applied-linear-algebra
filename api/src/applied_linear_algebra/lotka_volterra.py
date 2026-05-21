"""Discrete-time linearized Lotka-Volterra (rabbits and foxes).

Simulates a 2-state linear dynamical system

  X[t+1] = A X[t] + u

starting from X[0] = (rabbits, foxes). The original Project_28 fixed
A = [[1.9, -8], [0.1, 0.1]] and compared two policies (with vs. without
constant predator removal). This module generalizes: any 2x2 transition
matrix, optional constant intervention vector, arbitrary horizon.

This is a *linearization* of the true Lotka-Volterra ODE — it captures the
qualitative oscillation but cannot represent the conserved quantity that the
nonlinear continuous-time system has. The point is to show how a linear
discrete-time system propagates, not to compete with `scipy.integrate.odeint`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.floating]


@dataclass
class LotkaVolterraResult:
    trajectory: FloatArray  # shape (T+1, 2)
    eigenvalues: FloatArray  # complex spectrum of A
    horizon: int
    extinct: bool  # any population non-positive at any time?
    extinction_time: int | None


def simulate(
    A: NDArray[np.number],
    x0: NDArray[np.number],
    *,
    horizon: int = 20,
    intervention: NDArray[np.number] | None = None,
) -> LotkaVolterraResult:
    """Propagate X[t+1] = A X[t] + u for ``horizon`` steps."""
    A_arr = np.asarray(A, dtype=np.float64)
    if A_arr.shape != (2, 2):
        raise ValueError(f"A must be 2x2; got {A_arr.shape}.")
    x_arr = np.asarray(x0, dtype=np.float64).ravel()
    if x_arr.shape != (2,):
        raise ValueError(f"x0 must be length 2; got {x_arr.shape}.")
    if horizon < 1:
        raise ValueError("horizon must be positive.")
    u = (
        np.zeros(2, dtype=np.float64)
        if intervention is None
        else np.asarray(intervention, dtype=np.float64).ravel()
    )

    traj = np.zeros((horizon + 1, 2), dtype=np.float64)
    traj[0] = x_arr
    extinction_time: int | None = None
    for t in range(horizon):
        traj[t + 1] = A_arr @ traj[t] + u
        if extinction_time is None and (traj[t + 1] <= 0).any():
            extinction_time = t + 1

    eigvals = np.linalg.eigvals(A_arr)
    return LotkaVolterraResult(
        trajectory=traj,
        eigenvalues=eigvals,
        horizon=horizon,
        extinct=extinction_time is not None,
        extinction_time=extinction_time,
    )
