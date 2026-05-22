"""FastAPI app — six linear-algebra algorithms behind one HTTP surface.

Endpoints follow ``/api/<slug>/<action>`` so the frontend can map slugs from
the catalog to URL paths without ambiguity. CORS is wide-open by default
because there's nothing sensitive here — tighten ``ALLOWED_ORIGINS`` for
production deploys.
"""

from __future__ import annotations

import os

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from applied_linear_algebra import (
    __version__,
    autoregressive,
    clustering,
    fourier,
    hill_cipher,
    lotka_volterra,
    random_walk,
)

from api.schemas import (
    AutoregressiveRequest,
    AutoregressiveResponse,
    CatalogEntry,
    CatalogResponse,
    FourierRequest,
    FourierResponse,
    HealthResponse,
    HillEncryptRequest,
    HillEncryptResponse,
    IrisClusterRequest,
    IrisClusterResponse,
    LotkaVolterraRequest,
    LotkaVolterraResponse,
    RandomWalkRequest,
    RandomWalkResponse,
)


ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:3000,https://applied-linear-algebra.vercel.app"
).split(",")


app = FastAPI(
    title="applied-linear-algebra",
    description="Six applied linear-algebra algorithms exposed as JSON endpoints.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Meta
# ---------------------------------------------------------------------------


CATALOG: list[CatalogEntry] = [
    CatalogEntry(
        slug="clustering",
        name="Iris k-means clustering",
        description="From-scratch Lloyd's algorithm with k-means++ init on the canonical Iris dataset.",
        endpoint="/api/clustering/iris",
    ),
    CatalogEntry(
        slug="fourier",
        name="Fourier series approximation",
        description="Least-squares fit of truncated Fourier series to a target function.",
        endpoint="/api/fourier/fit",
    ),
    CatalogEntry(
        slug="hill_cipher",
        name="Hill cipher (modular)",
        description="Classical block cipher with proper modular matrix inverse over Z_p.",
        endpoint="/api/hill_cipher/encrypt",
    ),
    CatalogEntry(
        slug="autoregressive",
        name="Trend + seasonality forecast",
        description="Linear trend plus periodic dummies, fit via least squares; forecasts the airline-passengers series.",
        endpoint="/api/autoregressive/fit",
    ),
    CatalogEntry(
        slug="lotka_volterra",
        name="Predator-prey dynamics",
        description="Discrete-time linearized predator-prey system, parameterized by transition matrix and intervention.",
        endpoint="/api/lotka_volterra/simulate",
    ),
    CatalogEntry(
        slug="random_walk",
        name="Random walk on a graph",
        description="Markov chain on an undirected graph; compare empirical trajectory to closed-form stationary distribution.",
        endpoint="/api/random_walk/simulate",
    ),
]


@app.get("/", response_model=HealthResponse)
def root() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@app.get("/api/catalog", response_model=CatalogResponse)
def catalog() -> CatalogResponse:
    return CatalogResponse(algorithms=CATALOG)


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------


@app.post("/api/clustering/iris", response_model=IrisClusterResponse)
def cluster_iris(req: IrisClusterRequest) -> IrisClusterResponse:
    iris = clustering.iris_dataset()
    X = np.asarray(iris["data"], dtype=np.float64)
    result = clustering.fit_kmeans(
        X, k=req.k, max_iter=req.max_iter, seed=req.seed
    )
    return IrisClusterResponse(
        labels=result.labels.tolist(),
        centroids=result.centroids.tolist(),
        inertia=result.inertia,
        n_iter=result.n_iter,
        converged=result.converged,
        feature_names=iris["feature_names"],  # type: ignore[arg-type]
        target_names=iris["target_names"],  # type: ignore[arg-type]
        actual_labels=iris["target"],  # type: ignore[arg-type]
        data=iris["data"],  # type: ignore[arg-type]
    )


# ---------------------------------------------------------------------------
# Fourier
# ---------------------------------------------------------------------------


@app.post("/api/fourier/fit", response_model=FourierResponse)
def fit_fourier(req: FourierRequest) -> FourierResponse:
    x_eval = np.linspace(req.x_min, req.x_max, req.n_points)
    target_y = fourier.step_function(x_eval)
    result = fourier.fit_fourier(
        fourier.step_function,
        x_eval=x_eval,
        n_harmonics=req.n_harmonics,
        include_cosines=req.include_cosines,
        x_range=(req.x_min, req.x_max),
    )
    return FourierResponse(
        x=x_eval.tolist(),
        target=target_y.tolist(),
        fit=result.basis_y.tolist(),
        coefficients=result.coefficients.tolist(),
        residual_norm=result.residual_norm,
        n_harmonics=result.n_harmonics,
    )


# ---------------------------------------------------------------------------
# Hill cipher
# ---------------------------------------------------------------------------


@app.post("/api/hill_cipher/encrypt", response_model=HillEncryptResponse)
def hill_encrypt(req: HillEncryptRequest) -> HillEncryptResponse:
    try:
        A, b = hill_cipher.random_key(req.block_size, seed=req.seed)
        ciphertext = hill_cipher.encrypt(req.plaintext, A, b)
        decrypted = hill_cipher.decrypt(ciphertext, A, b)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    round_trip_ok = decrypted.rstrip() == req.plaintext.rstrip()
    return HillEncryptResponse(
        plaintext=req.plaintext,
        ciphertext=ciphertext.tolist(),
        key_A=A.tolist(),
        key_b=b.tolist(),
        modulus=hill_cipher.MODULUS,
        decrypted=decrypted,
        round_trip_ok=round_trip_ok,
    )


# ---------------------------------------------------------------------------
# Autoregressive
# ---------------------------------------------------------------------------


@app.post("/api/autoregressive/fit", response_model=AutoregressiveResponse)
def fit_autoregressive(req: AutoregressiveRequest) -> AutoregressiveResponse:
    y = np.asarray(
        req.series if req.series is not None else autoregressive.AIRLINE_PASSENGERS,
        dtype=np.float64,
    )
    if y.shape[0] < req.period * 2:
        raise HTTPException(
            status_code=422,
            detail=f"series must have at least {req.period * 2} observations (period={req.period}).",
        )
    result = autoregressive.fit_seasonal(y, period=req.period, horizon=req.horizon)
    return AutoregressiveResponse(
        historical=y.tolist(),
        fitted=result.fitted.tolist(),
        forecast=result.forecast.tolist(),
        coefficients=result.coefficients.tolist(),
        residual_norm=result.residual_norm,
        period=result.period,
        forecast_horizon=result.forecast_horizon,
    )


# ---------------------------------------------------------------------------
# Lotka-Volterra
# ---------------------------------------------------------------------------


@app.post("/api/lotka_volterra/simulate", response_model=LotkaVolterraResponse)
def simulate_lotka_volterra(req: LotkaVolterraRequest) -> LotkaVolterraResponse:
    try:
        result = lotka_volterra.simulate(
            A=req.A,
            x0=req.x0,
            horizon=req.horizon,
            intervention=req.intervention,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return LotkaVolterraResponse(
        trajectory=result.trajectory.tolist(),
        eigenvalues_real=result.eigenvalues.real.tolist(),
        eigenvalues_imag=result.eigenvalues.imag.tolist(),
        horizon=result.horizon,
        extinct=result.extinct,
        extinction_time=result.extinction_time,
    )


# ---------------------------------------------------------------------------
# Random walk
# ---------------------------------------------------------------------------


@app.post("/api/random_walk/simulate", response_model=RandomWalkResponse)
def simulate_random_walk(req: RandomWalkRequest) -> RandomWalkResponse:
    adjacency = req.adjacency if req.adjacency is not None else random_walk.DEFAULT_ADJACENCY
    try:
        result = random_walk.simulate(
            adjacency, start_vertex=req.start_vertex, steps=req.steps
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return RandomWalkResponse(
        trajectory=result.trajectory.tolist(),
        transition=result.transition.tolist(),
        stationary=result.stationary.tolist(),
        steps=result.steps,
        converged_to_stationary=result.converged_to_stationary,
    )
