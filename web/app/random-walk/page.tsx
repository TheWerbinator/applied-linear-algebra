"use client";

import { useState } from "react";
import AlgoLayout from "@/components/AlgoLayout";
import Plot from "@/components/Plot";
import { api } from "@/lib/api";
import type { RandomWalkResponse } from "@/lib/types";

export default function RandomWalkPage() {
  const [start, setStart] = useState(0);
  const [steps, setSteps] = useState(100);
  const [result, setResult] = useState<RandomWalkResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.simulateRandomWalk({ start_vertex: start, steps });
      setResult(r);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const n = result?.stationary.length ?? 0;
  const vertexLabels = result ? Array.from({ length: n }, (_, i) => `v${i}`) : [];

  const trajectoryTraces = result
    ? Array.from({ length: n }, (_, j) => ({
        x: result.trajectory.map((_, t) => t),
        y: result.trajectory.map((row) => row[j]),
        mode: "lines" as const,
        name: `v${j}`,
      }))
    : [];

  return (
    <AlgoLayout
      title="Random walk on a graph"
      subtitle="Markov chains · stationary distribution"
      description="Column-stochastic transition matrix T derived from the adjacency. The probability distribution X[t+1] = T X[t] converges to a stationary distribution π_i = deg(i) / Σ deg(j) for connected undirected graphs — readable straight from the degree sequence. Default graph is the 6-vertex Project_29 graph; you can change start vertex and step count."
      controls={
        <div className="space-y-3">
          <div>
            <label htmlFor="start">Start vertex</label>
            <input
              id="start"
              type="number"
              min={0}
              max={5}
              value={start}
              onChange={(e) => setStart(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <div>
            <label htmlFor="steps">Steps</label>
            <input
              id="steps"
              type="number"
              min={1}
              max={1000}
              value={steps}
              onChange={(e) => setSteps(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <button onClick={run} disabled={loading} className="w-full">
            {loading ? "Walking…" : "Simulate walk"}
          </button>
          {error && <p className="text-xs text-red-400">{error}</p>}
        </div>
      }
      visualization={
        result ? (
          <div className="space-y-6">
            <Plot
              data={trajectoryTraces}
              layout={{
                title: { text: "Probability mass per vertex over time" },
                xaxis: { title: { text: "step" } },
                yaxis: { title: { text: "P(X_t = v_i)" } },
                height: 320,
              }}
            />
            <Plot
              data={[
                {
                  x: vertexLabels,
                  y: result.trajectory[result.trajectory.length - 1],
                  type: "bar",
                  name: "empirical at last step",
                  marker: { color: "#38bdf8" },
                },
                {
                  x: vertexLabels,
                  y: result.stationary,
                  type: "bar",
                  name: "stationary π",
                  marker: { color: "#f472b6" },
                },
              ]}
              layout={{
                title: {
                  text: `Empirical vs stationary — converged: ${result.converged_to_stationary ? "yes" : "no"}`,
                },
                barmode: "group",
                yaxis: { title: { text: "probability" } },
                height: 320,
              }}
            />
          </div>
        ) : (
          <div className="flex h-96 items-center justify-center text-sm text-gray-500">
            Simulate to see the chain.
          </div>
        )
      }
    />
  );
}
