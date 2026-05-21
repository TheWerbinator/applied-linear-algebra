"""Autoregressive forecasting with a periodic component.

The original Project_20 fits

  y_t = α t + Σ_{j=1}^{P} β_j 𝟙[t mod P = j-1] + ε_t

where the design matrix has one trend column and P dummy columns (one per
month, for P = 12). Coefficients are recovered via least squares and the
forecast extrapolates the same form into the future.

Reframed here as a general "trend + seasonality" model so it's a clean
linear-model demo, not a one-off coursework script.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.floating]


@dataclass
class ARFit:
    coefficients: FloatArray
    fitted: FloatArray
    forecast: FloatArray
    forecast_horizon: int
    period: int
    residual_norm: float


def build_design(t: NDArray[np.integer], period: int) -> FloatArray:
    """Trend column followed by ``period`` dummy columns."""
    t_arr = np.asarray(t, dtype=np.int64)
    n = t_arr.shape[0]
    season = np.zeros((n, period), dtype=np.float64)
    for i, ti in enumerate(t_arr):
        season[i, int(ti % period)] = 1.0
    trend = t_arr.astype(np.float64).reshape(-1, 1)
    return np.hstack([trend, season])


def fit_seasonal(
    y: FloatArray,
    *,
    period: int = 12,
    horizon: int = 24,
) -> ARFit:
    """Fit y on (trend, seasonal dummies) and forecast ``horizon`` steps."""
    y_arr = np.asarray(y, dtype=np.float64).ravel()
    n = y_arr.shape[0]
    t = np.arange(n, dtype=np.int64)
    A = build_design(t, period)
    coef, *_ = np.linalg.lstsq(A, y_arr, rcond=None)

    fitted = A @ coef
    t_future = np.arange(n, n + horizon, dtype=np.int64)
    A_future = build_design(t_future, period)
    forecast = A_future @ coef
    residual = float(np.linalg.norm(fitted - y_arr))

    return ARFit(
        coefficients=coef,
        fitted=fitted,
        forecast=forecast,
        forecast_horizon=horizon,
        period=period,
        residual_norm=residual,
    )


# Canonical airline-passengers series (Box & Jenkins): 144 monthly counts,
# January 1949 through December 1960.
AIRLINE_PASSENGERS: list[int] = [
    112, 118, 132, 129, 121, 135, 148, 148, 136, 119, 104, 118,
    115, 126, 141, 135, 125, 149, 170, 170, 158, 133, 114, 140,
    145, 150, 178, 163, 172, 178, 199, 199, 184, 162, 146, 166,
    171, 180, 193, 181, 183, 218, 230, 242, 209, 191, 172, 194,
    196, 196, 236, 235, 229, 243, 264, 272, 237, 211, 180, 201,
    204, 188, 235, 227, 234, 264, 302, 293, 259, 229, 203, 229,
    242, 233, 267, 269, 270, 315, 364, 347, 312, 274, 237, 278,
    284, 277, 317, 313, 318, 374, 413, 405, 355, 306, 271, 306,
    315, 301, 356, 348, 355, 422, 465, 467, 404, 347, 305, 336,
    340, 318, 362, 348, 363, 435, 491, 505, 404, 359, 310, 337,
    360, 342, 406, 396, 420, 472, 548, 559, 463, 407, 362, 405,
    417, 391, 419, 461, 472, 535, 622, 606, 508, 461, 390, 432,
]
