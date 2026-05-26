import type {
  AutoregressiveResponse,
  CatalogResponse,
  FourierResponse,
  HillEncryptResponse,
  IrisClusterResponse,
  LotkaVolterraResponse,
  RandomWalkResponse,
} from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const resp = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`${resp.status} ${resp.statusText}: ${text}`);
  }
  return (await resp.json()) as T;
}

async function getJson<T>(path: string): Promise<T> {
  const resp = await fetch(`${BASE_URL}${path}`, { cache: "no-store" });
  if (!resp.ok) throw new Error(`${resp.status} ${resp.statusText}`);
  return (await resp.json()) as T;
}

export const api = {
  catalog: () => getJson<CatalogResponse>("/api/catalog"),

  clusterIris: (params: { k: number; seed: number; max_iter: number }) =>
    postJson<IrisClusterResponse>("/api/clustering/iris", params),

  fitFourier: (params: {
    n_harmonics: number;
    include_cosines: boolean;
    x_min: number;
    x_max: number;
    n_points: number;
  }) => postJson<FourierResponse>("/api/fourier/fit", params),

  hillEncrypt: (params: { plaintext: string; block_size: number; seed: number }) =>
    postJson<HillEncryptResponse>("/api/hill_cipher/encrypt", params),

  fitAutoregressive: (params: {
    period: number;
    horizon: number;
    series?: number[];
  }) => postJson<AutoregressiveResponse>("/api/autoregressive/fit", params),

  simulateLotkaVolterra: (params: {
    A: number[][];
    x0: number[];
    horizon: number;
    intervention?: number[];
  }) => postJson<LotkaVolterraResponse>("/api/lotka_volterra/simulate", params),

  simulateRandomWalk: (params: {
    adjacency?: number[][];
    start_vertex: number;
    steps: number;
  }) => postJson<RandomWalkResponse>("/api/random_walk/simulate", params),
};
