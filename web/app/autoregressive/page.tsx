"use client";

import { useState } from "react";
import AlgoLayout from "@/components/AlgoLayout";
import Plot from "@/components/Plot";
import { api } from "@/lib/api";
import type { AutoregressiveResponse } from "@/lib/types";

export default function AutoregressivePage() {
  const [period, setPeriod] = useState(12);
  const [horizon, setHorizon] = useState(24);
  const [result, setResult] = useState<AutoregressiveResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.fitAutoregressive({ period, horizon });
      setResult(r);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AlgoLayout
      title="Trend + seasonality forecast"
      subtitle="Time series · linear model with periodic dummies"
      description={
        "Fits y_t = α t + Σ β_j 𝟙[t mod P = j] via least squares on the Box & Jenkins airline-passengers series (144 monthly counts, Jan 1949 - Dec 1960). Extrapolates the same form into the future. The under-fit is informative: a linear trend can't capture the post-1955 acceleration, which a log-transform would handle."
      }
      controls={
        <div className="space-y-3">
          <div>
            <label htmlFor="p">Seasonal period</label>
            <input
              id="p"
              type="number"
              min={2}
              max={52}
              value={period}
              onChange={(e) => setPeriod(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <div>
            <label htmlFor="h">Forecast horizon</label>
            <input
              id="h"
              type="number"
              min={1}
              max={120}
              value={horizon}
              onChange={(e) => setHorizon(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <button onClick={run} disabled={loading} className="w-full">
            {loading ? "Fitting…" : "Fit + forecast"}
          </button>
          {error && <p className="text-xs text-red-400">{error}</p>}
        </div>
      }
      visualization={
        result ? (
          <Plot
            data={[
              {
                x: result.historical.map((_, i) => i),
                y: result.historical,
                mode: "lines+markers",
                name: "historical",
                line: { color: "#94a3b8", width: 1 },
                marker: { size: 4 },
              },
              {
                x: result.fitted.map((_, i) => i),
                y: result.fitted,
                mode: "lines",
                name: "fitted",
                line: { color: "#38bdf8", width: 2 },
              },
              {
                x: result.forecast.map(
                  (_, i) => result.historical.length + i,
                ),
                y: result.forecast,
                mode: "lines",
                name: "forecast",
                line: { color: "#f472b6", width: 2, dash: "dash" },
              },
            ]}
            layout={{
              title: {
                text: `Trend + ${result.period}-period seasonality, residual = ${result.residual_norm.toFixed(1)}`,
              },
              xaxis: { title: { text: "month index" } },
              yaxis: { title: { text: "passengers (thousands)" } },
              height: 480,
            }}
          />
        ) : (
          <div className="flex h-96 items-center justify-center text-sm text-gray-500">
            Fit to see historical + forecast.
          </div>
        )
      }
    />
  );
}
