"""Pydantic request/response schemas for the API."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Common
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    status: str
    version: str


class CatalogEntry(BaseModel):
    slug: str
    name: str
    description: str
    endpoint: str


class CatalogResponse(BaseModel):
    algorithms: list[CatalogEntry]


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------


class IrisClusterRequest(BaseModel):
    k: int = Field(3, ge=1, le=10)
    seed: int = Field(0, ge=0)
    max_iter: int = Field(300, ge=1, le=1000)


class IrisClusterResponse(BaseModel):
    labels: list[int]
    centroids: list[list[float]]
    inertia: float
    n_iter: int
    converged: bool
    feature_names: list[str]
    target_names: list[str]
    actual_labels: list[int]
    data: list[list[float]]


# ---------------------------------------------------------------------------
# Fourier
# ---------------------------------------------------------------------------


class FourierRequest(BaseModel):
    n_harmonics: int = Field(25, ge=1, le=200)
    include_cosines: bool = False
    x_min: float = -10.0
    x_max: float = 10.0
    n_points: int = Field(500, ge=50, le=2000)


class FourierResponse(BaseModel):
    x: list[float]
    target: list[float]
    fit: list[float]
    coefficients: list[float]
    residual_norm: float
    n_harmonics: int


# ---------------------------------------------------------------------------
# Hill cipher
# ---------------------------------------------------------------------------


class HillEncryptRequest(BaseModel):
    plaintext: str = Field(..., min_length=1, max_length=2000)
    block_size: int = Field(3, ge=2, le=6)
    seed: int = Field(0, ge=0)


class HillEncryptResponse(BaseModel):
    plaintext: str
    ciphertext: list[list[int]]
    key_A: list[list[int]]
    key_b: list[int]
    modulus: int
    decrypted: str
    round_trip_ok: bool


# ---------------------------------------------------------------------------
# Autoregressive
# ---------------------------------------------------------------------------


class AutoregressiveRequest(BaseModel):
    period: int = Field(12, ge=2, le=52)
    horizon: int = Field(24, ge=1, le=120)
    series: list[float] | None = None


class AutoregressiveResponse(BaseModel):
    historical: list[float]
    fitted: list[float]
    forecast: list[float]
    coefficients: list[float]
    residual_norm: float
    period: int
    forecast_horizon: int


# ---------------------------------------------------------------------------
# Lotka-Volterra
# ---------------------------------------------------------------------------


class LotkaVolterraRequest(BaseModel):
    A: list[list[float]] = Field(
        default=[[1.9, -8.0], [0.1, 0.1]],
        min_length=2,
        max_length=2,
    )
    x0: list[float] = Field(default=[100.0, 12.0], min_length=2, max_length=2)
    horizon: int = Field(20, ge=1, le=200)
    intervention: list[float] | None = Field(default=None)


class LotkaVolterraResponse(BaseModel):
    trajectory: list[list[float]]
    eigenvalues_real: list[float]
    eigenvalues_imag: list[float]
    horizon: int
    extinct: bool
    extinction_time: int | None


# ---------------------------------------------------------------------------
# Random walk
# ---------------------------------------------------------------------------


class RandomWalkRequest(BaseModel):
    adjacency: list[list[int]] | None = None
    start_vertex: int = Field(0, ge=0)
    steps: int = Field(100, ge=1, le=1000)


class RandomWalkResponse(BaseModel):
    trajectory: list[list[float]]
    transition: list[list[float]]
    stationary: list[float]
    steps: int
    converged_to_stationary: bool
