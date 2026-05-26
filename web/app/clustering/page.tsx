"use client";

import { useState } from "react";
import AlgoLayout from "@/components/AlgoLayout";
import Plot from "@/components/Plot";
import { api } from "@/lib/api";
import type { IrisClusterResponse } from "@/lib/types";

const CLUSTER_COLORS = ["#38bdf8", "#f472b6", "#facc15", "#34d399", "#a78bfa"];

export default function ClusteringPage() {
  const [k, setK] = useState(3);
  const [seed, setSeed] = useState(0);
  const [result, setResult] = useState<IrisClusterResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.clusterIris({ k, seed, max_iter: 300 });
      setResult(r);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  // Petal length (col 2) vs petal width (col 3) — the most separable pair.
  const traces = result
    ? Array.from({ length: k }, (_, j) => ({
        x: result.data.filter((_, i) => result.labels[i] === j).map((r) => r[2]),
        y: result.data.filter((_, i) => result.labels[i] === j).map((r) => r[3]),
        mode: "markers" as const,
        type: "scatter" as const,
        name: `cluster ${j}`,
        marker: { color: CLUSTER_COLORS[j % CLUSTER_COLORS.length], size: 8 },
      })).concat([
        {
          x: result.centroids.map((c) => c[2]),
          y: result.centroids.map((c) => c[3]),
          mode: "markers" as const,
          type: "scatter" as const,
          name: "centroids",
          marker: {
            color: "#fff",
            size: 16,
            symbol: "x" as never,
            line: { width: 2, color: "#000" },
          },
        },
      ])
    : [];

  return (
    <AlgoLayout
      title="Iris k-means clustering"
      subtitle="Unsupervised learning · Lloyd's algorithm"
      description="K-means++ initialization, repeated assign/update steps until centroids stabilize. Plotted on petal length × petal width (the two most separable features). White ✕ marks final centroid positions."
      controls={
        <div className="space-y-3">
          <div>
            <label htmlFor="k">Clusters (k)</label>
            <input
              id="k"
              type="number"
              min={1}
              max={10}
              value={k}
              onChange={(e) => setK(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <div>
            <label htmlFor="seed">Random seed</label>
            <input
              id="seed"
              type="number"
              min={0}
              value={seed}
              onChange={(e) => setSeed(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <button onClick={run} disabled={loading} className="w-full">
            {loading ? "Running…" : "Run k-means"}
          </button>
          {error && <p className="text-xs text-red-400">{error}</p>}
        </div>
      }
      visualization={
        result ? (
          <Plot
            data={traces}
            layout={{
              title: "Iris clusters (petal length vs petal width)",
              xaxis: { title: "petal length (cm)" },
              yaxis: { title: "petal width (cm)" },
              height: 480,
            }}
          />
        ) : (
          <div className="flex h-96 items-center justify-center text-sm text-gray-500">
            Run the algorithm to see clusters.
          </div>
        )
      }
      details={
        result && (
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <Stat label="Inertia" value={result.inertia.toFixed(2)} />
            <Stat label="Iterations" value={result.n_iter} />
            <Stat label="Converged" value={result.converged ? "yes" : "no"} />
            <Stat label="k" value={k} />
          </div>
        )
      }
    />
  );
}

function Stat({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded border border-border bg-background p-3">
      <div className="text-xs uppercase tracking-wide text-gray-500">{label}</div>
      <div className="mt-1 font-mono text-lg text-gray-100">{value}</div>
    </div>
  );
}
