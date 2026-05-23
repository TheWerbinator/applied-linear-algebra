"""Tests for the random-walk Markov chain."""

from __future__ import annotations

import numpy as np
import pytest

from applied_linear_algebra import random_walk


def test_transition_matrix_columns_sum_to_one() -> None:
    A = np.asarray(random_walk.DEFAULT_ADJACENCY, dtype=np.float64)
    T = random_walk.transition_matrix(A)
    np.testing.assert_allclose(T.sum(axis=0), 1.0, atol=1e-12)


def test_stationary_sums_to_one() -> None:
    pi = random_walk.stationary_distribution(random_walk.DEFAULT_ADJACENCY)
    assert pi.sum() == pytest.approx(1.0)


def test_stationary_matches_degree_ratio() -> None:
    """π_i = deg(i) / Σ deg(j) for undirected graphs."""
    A = np.asarray(random_walk.DEFAULT_ADJACENCY, dtype=np.float64)
    pi = random_walk.stationary_distribution(A)
    degrees = A.sum(axis=1)
    np.testing.assert_allclose(pi, degrees / degrees.sum())


def test_trajectory_each_row_sums_to_one() -> None:
    result = random_walk.simulate(random_walk.DEFAULT_ADJACENCY, steps=20)
    np.testing.assert_allclose(result.trajectory.sum(axis=1), 1.0, atol=1e-10)


def test_long_walk_converges_to_stationary() -> None:
    result = random_walk.simulate(random_walk.DEFAULT_ADJACENCY, steps=500)
    # For this connected, non-bipartite graph the chain converges.
    diff = float(np.linalg.norm(result.trajectory[-1] - result.stationary))
    assert diff < 1e-3


def test_rejects_isolated_vertex() -> None:
    bad = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
    with pytest.raises(ValueError):
        random_walk.transition_matrix(bad)


def test_rejects_out_of_range_start() -> None:
    with pytest.raises(ValueError):
        random_walk.simulate(random_walk.DEFAULT_ADJACENCY, start_vertex=42)
