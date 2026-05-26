/** Response types matching the FastAPI backend's Pydantic schemas. */

export interface CatalogEntry {
  slug: string;
  name: string;
  description: string;
  endpoint: string;
}

export interface CatalogResponse {
  algorithms: CatalogEntry[];
}

export interface IrisClusterResponse {
  labels: number[];
  centroids: number[][];
  inertia: number;
  n_iter: number;
  converged: boolean;
  feature_names: string[];
  target_names: string[];
  actual_labels: number[];
  data: number[][];
}

export interface FourierResponse {
  x: number[];
  target: number[];
  fit: number[];
  coefficients: number[];
  residual_norm: number;
  n_harmonics: number;
}

export interface HillEncryptResponse {
  plaintext: string;
  ciphertext: number[][];
  key_A: number[][];
  key_b: number[];
  modulus: number;
  decrypted: string;
  round_trip_ok: boolean;
}

export interface AutoregressiveResponse {
  historical: number[];
  fitted: number[];
  forecast: number[];
  coefficients: number[];
  residual_norm: number;
  period: number;
  forecast_horizon: number;
}

export interface LotkaVolterraResponse {
  trajectory: number[][];
  eigenvalues_real: number[];
  eigenvalues_imag: number[];
  horizon: number;
  extinct: boolean;
  extinction_time: number | null;
}

export interface RandomWalkResponse {
  trajectory: number[][];
  transition: number[][];
  stationary: number[];
  steps: number;
  converged_to_stationary: boolean;
}
