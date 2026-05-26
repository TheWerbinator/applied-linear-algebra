"use client";

import { useState } from "react";
import AlgoLayout from "@/components/AlgoLayout";
import Plot from "@/components/Plot";
import { api } from "@/lib/api";
import type { FourierResponse } from "@/lib/types";

export default function FourierPage() {
  const [nHarmonics, setNHarmonics] = useState(25);
  const [includeCosines, setIncludeCosines] = useState(false);
  const [xMin, setXMin] = useState(-10);
  const [xMax, setXMax] = useState(10);
  const [result, setResult] = useState<FourierResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.fitFourier({
        n_harmonics: nHarmonics,
        include_cosines: includeCosines,
        x_min: xMin,
        x_max: xMax,
        n_points: 500,
      });
      setResult(r);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AlgoLayout
      title="Fourier series approximation"
      subtitle="Function approximation · least-squares"
      description="Approximates a square wave by a truncated sum of sine harmonics. The classic Gibbs overshoot near each jump is the obstruction — adding harmonics makes overshoot narrower but not shorter."
      controls={
        <div className="space-y-3">
          <div>
            <label htmlFor="n">Harmonics</label>
            <input
              id="n"
              type="number"
              min={1}
              max={200}
              value={nHarmonics}
              onChange={(e) => setNHarmonics(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-300">
            <input
              id="cos"
              type="checkbox"
              checked={includeCosines}
              onChange={(e) => setIncludeCosines(e.target.checked)}
            />
            <label htmlFor="cos" className="!normal-case !text-sm !tracking-normal">
              include cosines
            </label>
          </div>
          <div>
            <label htmlFor="xmin">x min</label>
            <input
              id="xmin"
              type="number"
              value={xMin}
              onChange={(e) => setXMin(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <div>
            <label htmlFor="xmax">x max</label>
            <input
              id="xmax"
              type="number"
              value={xMax}
              onChange={(e) => setXMax(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <button onClick={run} disabled={loading} className="w-full">
            {loading ? "Fitting…" : "Fit"}
          </button>
          {error && <p className="text-xs text-red-400">{error}</p>}
        </div>
      }
      visualization={
        result ? (
          <Plot
            data={[
              {
                x: result.x,
                y: result.target,
                mode: "lines",
                name: "target",
                line: { color: "#f472b6", width: 2, dash: "dot" },
              },
              {
                x: result.x,
                y: result.fit,
                mode: "lines",
                name: "fit",
                line: { color: "#38bdf8", width: 2 },
              },
            ]}
            layout={{
              title: `Fourier fit, ${result.n_harmonics} harmonics, residual = ${result.residual_norm.toFixed(3)}`,
              xaxis: { title: "x" },
              yaxis: { title: "f(x)" },
              height: 480,
            }}
          />
        ) : (
          <div className="flex h-96 items-center justify-center text-sm text-gray-500">
            Fit to see the approximation.
          </div>
        )
      }
    />
  );
}
