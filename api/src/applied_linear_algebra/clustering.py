"""K-means clustering — from-scratch implementation plus the Iris benchmark.

The original coursework imported ``sklearn.cluster.KMeans``. Here we implement
Lloyd's algorithm directly so the linear-algebra mechanics are inspectable,
then verify against sklearn as a sanity check.

The math: alternate two steps until labels stop changing.

  Assignment step:  l_i = argmin_j ‖ x_i - c_j ‖²
  Update step:      c_j = (1 / |S_j|) Σ_{i ∈ S_j} x_i

Each iteration monotonically decreases the inertia
J = Σ_i ‖ x_i - c_{l_i} ‖², so the algorithm converges (to a local minimum
that depends on the initialization).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from sklearn.datasets import load_iris


FloatArray = NDArray[np.floating]
IntArray = NDArray[np.integer]


@dataclass
class KMeansResult:
    """Output of ``fit_kmeans``."""

    labels: IntArray
    centroids: FloatArray
    inertia: float
    n_iter: int
    converged: bool


def _kmeans_pp_init(
    X: FloatArray, k: int, rng: np.random.Generator
) -> FloatArray:
    """K-means++ seeding: pick centers proportional to squared distance.

    Empirically reduces the chance of converging to a poor local minimum
    compared to uniform random initialization.
    """
    n = X.shape[0]
    centers = np.empty((k, X.shape[1]), dtype=np.float64)
    centers[0] = X[rng.integers(0, n)]
    for j in range(1, k):
        dists = np.min(
            np.linalg.norm(X[:, None, :] - centers[:j][None, :, :], axis=2) ** 2,
            axis=1,
        )
        total = dists.sum()
        if total == 0:
            centers[j] = X[rng.integers(0, n)]
            continue
        probs = dists / total
        idx = int(rng.choice(n, p=probs))
        centers[j] = X[idx]
    return centers


def fit_kmeans(
    X: NDArray[np.number],
    k: int,
    *,
    max_iter: int = 300,
    tol: float = 1e-4,
    seed: int = 0,
) -> KMeansResult:
    """Lloyd's algorithm with k-means++ initialization.

    Parameters
    ----------
    X : (n, d) array of samples.
    k : number of clusters; must be in [1, n].
    max_iter : hard cap on iterations.
    tol : convergence threshold on centroid shift (Frobenius norm).
    seed : RNG seed for initialization reproducibility.
    """
    X_arr = np.asarray(X, dtype=np.float64)
    if X_arr.ndim != 2:
        raise ValueError(f"X must be 2-D, got shape {X_arr.shape}.")
    n, _ = X_arr.shape
    if not (1 <= k <= n):
        raise ValueError(f"k must be in [1, n]; got k={k}, n={n}.")

    rng = np.random.default_rng(seed)
    centers = _kmeans_pp_init(X_arr, k, rng)

    labels = np.zeros(n, dtype=np.int64)
    converged = False
    for it in range(max_iter):
        dists = np.linalg.norm(X_arr[:, None, :] - centers[None, :, :], axis=2)
        new_labels = np.argmin(dists, axis=1)
        new_centers = np.empty_like(centers)
        for j in range(k):
            members = X_arr[new_labels == j]
            new_centers[j] = members.mean(axis=0) if len(members) else centers[j]
        shift = float(np.linalg.norm(new_centers - centers))
        centers = new_centers
        labels = new_labels.astype(np.int64)
        if shift < tol:
            converged = True
            break

    inertia = float(
        np.sum(
            np.linalg.norm(X_arr - centers[labels], axis=1) ** 2
        )
    )
    return KMeansResult(
        labels=labels,
        centroids=centers,
        inertia=inertia,
        n_iter=it + 1,
        converged=converged,
    )


def iris_dataset() -> dict[str, list[float] | list[str] | list[list[float]] | list[int]]:
    """Return the canonical Iris dataset as JSON-serializable lists."""
    data = load_iris()
    return {
        "data": data.data.tolist(),
        "target": data.target.tolist(),
        "target_names": list(data.target_names),
        "feature_names": list(data.feature_names),
    }
