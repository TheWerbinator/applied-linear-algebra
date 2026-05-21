"""Random walk on a graph — Markov chain via repeated transition-matrix products.

For an undirected graph with adjacency matrix A, the column-stochastic
transition matrix T is

  T[j, i] = A[i, j] / deg(i)   (probability of moving from vertex i to j)

The probability distribution after t steps starting from state x_0 is

  X[t] = T^t x_0.

As t → ∞ the chain converges to the stationary distribution
π_i = deg(i) / Σ deg(j) (for connected undirected graphs), which can be read
off directly from the degree sequence — Project_29's punchline. We expose
both the per-step trajectory and the analytic stationary distribution so the
two can be compared.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.floating]
IntArray = NDArray[np.integer]


@dataclass
class RandomWalkResult:
    trajectory: FloatArray  # shape (steps+1, n_vertices)
    transition: FloatArray
    stationary: FloatArray
    steps: int
    converged_to_stationary: bool


def transition_matrix(adjacency: NDArray[np.number]) -> FloatArray:
    """Column-stochastic random-walk transition matrix from an adjacency matrix.

    Rejects vertices with degree 0 (no outgoing edge defined) because the
    walk would have nowhere to go.
    """
    A = np.asarray(adjacency, dtype=np.float64)
    n = A.shape[0]
    if A.shape != (n, n):
        raise ValueError(f"Adjacency must be square; got {A.shape}.")
    degrees = A.sum(axis=1)
    if np.any(degrees == 0):
        raise ValueError("Graph has an isolated vertex; transition undefined.")
    return (A.T / degrees).astype(np.float64)


def stationary_distribution(adjacency: NDArray[np.number]) -> FloatArray:
    """π_i = deg(i) / Σ deg(j) — closed form for connected undirected graphs."""
    A = np.asarray(adjacency, dtype=np.float64)
    degrees = A.sum(axis=1)
    return degrees / degrees.sum()


def simulate(
    adjacency: NDArray[np.number],
    start_vertex: int = 0,
    *,
    steps: int = 100,
    convergence_tol: float = 1e-6,
) -> RandomWalkResult:
    """Run the walk for ``steps`` iterations and record the distribution each step."""
    A = np.asarray(adjacency, dtype=np.float64)
    n = A.shape[0]
    if not 0 <= start_vertex < n:
        raise ValueError(f"start_vertex must be in [0, {n}); got {start_vertex}.")

    T = transition_matrix(A)
    pi = stationary_distribution(A)

    trajectory = np.zeros((steps + 1, n), dtype=np.float64)
    trajectory[0, start_vertex] = 1.0
    for t in range(steps):
        trajectory[t + 1] = T @ trajectory[t]

    converged = bool(np.linalg.norm(trajectory[-1] - pi) < convergence_tol)
    return RandomWalkResult(
        trajectory=trajectory,
        transition=T,
        stationary=pi,
        steps=steps,
        converged_to_stationary=converged,
    )


# Project_29 graph: 6-vertex undirected graph used in the original coursework.
DEFAULT_ADJACENCY: list[list[int]] = [
    [0, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 1, 0],
]
