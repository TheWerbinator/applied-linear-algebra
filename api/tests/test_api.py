"""FastAPI endpoint smoke tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_root(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_healthz(client: TestClient) -> None:
    resp = client.get("/healthz")
    assert resp.status_code == 200


def test_catalog_lists_six_algorithms(client: TestClient) -> None:
    resp = client.get("/api/catalog")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["algorithms"]) == 6
    slugs = {a["slug"] for a in body["algorithms"]}
    assert slugs == {
        "clustering",
        "fourier",
        "hill_cipher",
        "autoregressive",
        "lotka_volterra",
        "random_walk",
    }


def test_clustering_endpoint(client: TestClient) -> None:
    resp = client.post("/api/clustering/iris", json={"k": 3, "seed": 0})
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["labels"]) == 150
    assert len(body["centroids"]) == 3
    assert body["n_iter"] > 0


def test_fourier_endpoint(client: TestClient) -> None:
    resp = client.post(
        "/api/fourier/fit",
        json={"n_harmonics": 10, "x_min": -5.0, "x_max": 5.0, "n_points": 200},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["x"]) == 200
    assert len(body["fit"]) == 200
    assert body["n_harmonics"] == 10


def test_hill_cipher_endpoint_round_trip(client: TestClient) -> None:
    resp = client.post(
        "/api/hill_cipher/encrypt",
        json={"plaintext": "linear algebra", "block_size": 3, "seed": 0},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["round_trip_ok"] is True
    assert body["modulus"] == 101


def test_autoregressive_endpoint_default_series(client: TestClient) -> None:
    resp = client.post(
        "/api/autoregressive/fit",
        json={"period": 12, "horizon": 24},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["historical"]) == 144
    assert len(body["forecast"]) == 24


def test_autoregressive_endpoint_rejects_short_series(client: TestClient) -> None:
    resp = client.post(
        "/api/autoregressive/fit",
        json={"period": 12, "horizon": 24, "series": [1.0, 2.0, 3.0]},
    )
    assert resp.status_code == 422


def test_lotka_volterra_endpoint(client: TestClient) -> None:
    resp = client.post(
        "/api/lotka_volterra/simulate",
        json={
            "A": [[1.9, -8.0], [0.1, 0.1]],
            "x0": [100.0, 12.0],
            "horizon": 20,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["trajectory"]) == 21
    assert body["horizon"] == 20


def test_random_walk_endpoint_default_graph(client: TestClient) -> None:
    resp = client.post(
        "/api/random_walk/simulate",
        json={"start_vertex": 0, "steps": 50},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["trajectory"]) == 51
    assert len(body["stationary"]) == 6


def test_random_walk_endpoint_rejects_isolated_vertex(client: TestClient) -> None:
    resp = client.post(
        "/api/random_walk/simulate",
        json={
            "adjacency": [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
            "start_vertex": 0,
            "steps": 10,
        },
    )
    assert resp.status_code == 422
