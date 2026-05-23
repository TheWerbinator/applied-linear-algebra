"""Tests for the trend + seasonality model."""

from __future__ import annotations

import numpy as np

from applied_linear_algebra import autoregressive


def test_airline_passengers_known_length() -> None:
    assert len(autoregressive.AIRLINE_PASSENGERS) == 144


def test_fit_recovers_known_trend_and_seasonality() -> None:
    """Synthesize y_t = 2 t + S_t and verify the slope ≈ 2."""
    n = 60
    period = 12
    trend = 2.0 * np.arange(n)
    seasonal = np.tile([10, -5, 0, 15, -10, 20, 5, -15, 0, 10, -5, 25], n // period)
    y = trend + seasonal
    fit = autoregressive.fit_seasonal(y, period=period, horizon=12)
    # Trend coefficient is the first entry by construction.
    assert abs(fit.coefficients[0] - 2.0) < 1e-6
    # Fitted values must equal y up to numerical noise (rank = n).
    np.testing.assert_allclose(fit.fitted, y, atol=1e-6)


def test_forecast_extrapolates_trend() -> None:
    """For a purely linear series y_t = 3 t + 1, forecast should continue."""
    n = 48
    period = 12
    y = 3.0 * np.arange(n) + 1.0
    fit = autoregressive.fit_seasonal(y, period=period, horizon=24)
    t_future = np.arange(n, n + 24)
    expected = 3.0 * t_future + 1.0
    np.testing.assert_allclose(fit.forecast, expected, atol=1e-6)


def test_fit_returns_correct_shapes() -> None:
    y = np.asarray(autoregressive.AIRLINE_PASSENGERS, dtype=np.float64)
    fit = autoregressive.fit_seasonal(y, period=12, horizon=24)
    assert fit.fitted.shape == (144,)
    assert fit.forecast.shape == (24,)
    assert fit.coefficients.shape == (1 + 12,)  # trend + 12 month dummies
    assert fit.residual_norm > 0
