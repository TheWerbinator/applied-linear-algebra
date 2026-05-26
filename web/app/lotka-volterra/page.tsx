"use client";

import { useState } from "react";
import AlgoLayout from "@/components/AlgoLayout";
import Plot from "@/components/Plot";
import { api } from "@/lib/api";
import type { LotkaVolterraResponse } from "@/lib/types";

export default function LotkaVolterraPage() {
  const [a00, setA00] = useState(1.9);
  const [a01, setA01] = useState(-8.0);
  const [a10, setA10] = useState(0.1);
  const [a11, setA11] = useState(0.1);
  const [x0Rabbits, setX0Rabbits] = useState(100);
  const [x0Foxes, setX0Foxes] = useState(12);
  const [horizon, setHorizon] = useState(20);
  const [withIntervention, setWithIntervention] = useState(false);
  const [result, setResult] = useState<LotkaVolterraResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.simulateLotkaVolterra({
        A: [
          [a00, a01],
          [a10, a11],
        ],
        x0: [x0Rabbits, x0Foxes],
        horizon,
        intervention: withIntervention ? [-0.1, 0] : undefined,
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
      title="Predator-prey dynamics"
      subtitle="Dynamical systems · linearized Lotka-Volterra"
      description="Discrete-time linear system X[t+1] = A X[t] + u with optional constant intervention u. Toggle intervention to see how a small per-step adjustment changes whether populations stabilize or collapse. Eigenvalues of A determine the qualitative behavior — complex pair → oscillation, |λ| > 1 → growth, |λ| < 1 → decay."
      controls={
        <div className="space-y-3 text-sm">
          <div className="space-y-2">
            <label>Transition matrix A</label>
            <div className="grid grid-cols-2 gap-2">
              <input
                type="number"
                step={0.1}
                value={a00}
                onChange={(e) => setA00(Number(e.target.value))}
              />
              <input
                type="number"
                step={0.1}
                value={a01}
                onChange={(e) => setA01(Number(e.target.value))}
              />
              <input
                type="number"
                step={0.1}
                value={a10}
                onChange={(e) => setA10(Number(e.target.value))}
              />
              <input
                type="number"
                step={0.1}
                value={a11}
                onChange={(e) => setA11(Number(e.target.value))}
              />
            </div>
          </div>
          <div>
            <label>Initial state (rabbits, foxes)</label>
            <div className="mt-1 grid grid-cols-2 gap-2">
              <input
                type="number"
                value={x0Rabbits}
                onChange={(e) => setX0Rabbits(Number(e.target.value))}
              />
              <input
                type="number"
                value={x0Foxes}
                onChange={(e) => setX0Foxes(Number(e.target.value))}
              />
            </div>
          </div>
          <div>
            <label htmlFor="h">Horizon</label>
            <input
              id="h"
              type="number"
              min={1}
              max={200}
              value={horizon}
              onChange={(e) => setHorizon(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <div className="flex items-center gap-2 text-gray-300">
            <input
              id="iv"
              type="checkbox"
              checked={withIntervention}
              onChange={(e) => setWithIntervention(e.target.checked)}
            />
            <label htmlFor="iv" className="!normal-case !tracking-normal">
              constant intervention (–0.1 rabbits/step)
            </label>
          </div>
          <button onClick={run} disabled={loading} className="w-full">
            {loading ? "Simulating…" : "Simulate"}
          </button>
          {error && <p className="text-xs text-red-400">{error}</p>}
        </div>
      }
      visualization={
        result ? (
          <Plot
            data={[
              {
                x: result.trajectory.map((_, i) => i),
                y: result.trajectory.map((row) => row[0]),
                mode: "lines+markers",
                name: "rabbits",
                line: { color: "#38bdf8", width: 2 },
              },
              {
                x: result.trajectory.map((_, i) => i),
                y: result.trajectory.map((row) => row[1]),
                mode: "lines+markers",
                name: "foxes",
                line: { color: "#f472b6", width: 2 },
              },
            ]}
            layout={{
              title: {
                text: `Trajectory, eigenvalues = ${result.eigenvalues_real
                  .map((re, i) => formatEigenvalue(re, result.eigenvalues_imag[i]))
                  .join(", ")}`,
              },
              xaxis: { title: { text: "time step" } },
              yaxis: { title: { text: "population (thousands)" } },
              height: 480,
            }}
          />
        ) : (
          <div className="flex h-96 items-center justify-center text-sm text-gray-500">
            Simulate to see the trajectory.
          </div>
        )
      }
      details={
        result?.extinct && (
          <div className="text-red-400">
            ⚠ Population went non-positive at step {result.extinction_time} — the
            linear model has produced extinction.
          </div>
        )
      }
    />
  );
}

function formatEigenvalue(re: number, im: number): string {
  if (Math.abs(im) < 1e-9) return re.toFixed(3);
  const sign = im >= 0 ? "+" : "-";
  return `${re.toFixed(3)} ${sign} ${Math.abs(im).toFixed(3)}i`;
}
