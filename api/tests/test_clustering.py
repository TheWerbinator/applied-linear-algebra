"""Tests for the k-means implementation."""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

from applied_linear_algebra import clustering


def test_kmeans_separates_well_separated_clusters() -> None:
    rng = np.random.default_rng(0)
    a = rng.normal(loc=(0, 0), scale=0.1, size=(100, 2))
    b = rng.normal(loc=(10, 10), scale=0.1, size=(100, 2))
    c = rng.normal(loc=(0, 10), scale=0.1, size=(100, 2))
    X = np.vstack([a, b, c])
    truth = np.repeat([0, 1, 2], 100)

    result = clustering.fit_kmeans(X, k=3, seed=0)
    ari = adjusted_rand_score(truth, result.labels)
    assert ari > 0.99


def test_kmeans_converges_within_max_iter() -> None:
    rng = np.random.default_rng(0)
    X = rng.normal(size=(50, 2))
    result = clustering.fit_kmeans(X, k=3, max_iter=300, seed=0)
    assert result.n_iter <= 300


def test_kmeans_rejects_invalid_k() -> None:
    X = np.zeros((5, 2))
    with pytest.raises(ValueError):
        clustering.fit_kmeans(X, k=0)
    with pytest.raises(ValueError):
        clustering.fit_kmeans(X, k=10)


def test_kmeans_matches_sklearn_inertia_within_tolerance() -> None:
    """Our inertia should be at most ~10% worse than sklearn's on a clean problem."""
    rng = np.random.default_rng(42)
    X = np.vstack([
        rng.normal(loc=(0, 0), scale=0.3, size=(50, 2)),
        rng.normal(loc=(5, 5), scale=0.3, size=(50, 2)),
        rng.normal(loc=(0, 5), scale=0.3, size=(50, 2)),
    ])
    ours = clustering.fit_kmeans(X, k=3, seed=0)
    skl = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
    assert ours.inertia <= 1.1 * skl.inertia_


def test_iris_dataset_shape() -> None:
    data = clustering.iris_dataset()
    assert len(data["data"]) == 150
    assert all(len(row) == 4 for row in data["data"])
    assert len(data["target"]) == 150
    assert data["target_names"] == ["setosa", "versicolor", "virginica"]


@given(
    n=st.integers(min_value=10, max_value=100),
    k=st.integers(min_value=2, max_value=5),
)
@settings(max_examples=15, deadline=None)
def test_kmeans_property_labels_in_range(n: int, k: int) -> None:
    if n < k:
        return
    rng = np.random.default_rng(0)
    X = rng.normal(size=(n, 3))
    result = clustering.fit_kmeans(X, k=k, seed=0)
    assert result.labels.shape == (n,)
    assert set(np.unique(result.labels).tolist()).issubset(set(range(k)))
    assert result.centroids.shape == (k, 3)
