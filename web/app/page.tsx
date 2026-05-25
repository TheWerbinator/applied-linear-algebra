import AlgoCard from "@/components/AlgoCard";

export default function Home() {
  return (
    <div className="space-y-10">
      <section>
        <h1 className="text-4xl font-semibold text-gray-100">
          Applied Linear Algebra
        </h1>
        <p className="mt-4 max-w-3xl text-base leading-relaxed text-gray-400">
          Six applied linear-algebra algorithms — clustering, Fourier
          approximation, modular cryptography, time-series forecasting,
          dynamical systems, and Markov chains — implemented as a typed
          Python package, exposed via a FastAPI service, and visualized in
          this Next.js client. Pick one to play with.
        </p>
        <div className="mt-4 flex flex-wrap gap-3 text-xs text-gray-500">
          <span className="rounded border border-border px-2 py-1">
            numpy · scikit-learn
          </span>
          <span className="rounded border border-border px-2 py-1">
            FastAPI · Pydantic v2 · Fly.io
          </span>
          <span className="rounded border border-border px-2 py-1">
            Next.js 14 · Plotly · Vercel
          </span>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <AlgoCard
          href="/clustering"
          topic="Unsupervised learning"
          title="Iris k-means clustering"
          blurb="From-scratch Lloyd's algorithm with k-means++ initialization, compared to the true Iris labels."
        />
        <AlgoCard
          href="/fourier"
          topic="Function approximation"
          title="Fourier series fit"
          blurb="Least-squares approximation of a target function as a truncated sum of harmonics."
        />
        <AlgoCard
          href="/hill-cipher"
          topic="Cryptography"
          title="Hill cipher (modular)"
          blurb="Classical block cipher with a proper modular matrix inverse over Z_p — no floating-point fragility."
        />
        <AlgoCard
          href="/autoregressive"
          topic="Time series"
          title="Trend + seasonality forecast"
          blurb="Linear trend plus periodic dummies on the airline-passengers series; forecasts 24 months ahead."
        />
        <AlgoCard
          href="/lotka-volterra"
          topic="Dynamical systems"
          title="Predator-prey dynamics"
          blurb="Linearized Lotka-Volterra. Tune the transition matrix and intervention vector; watch the trajectory and eigenvalues."
        />
        <AlgoCard
          href="/random-walk"
          topic="Markov chains"
          title="Random walk on a graph"
          blurb="Repeated transition-matrix products converge to the stationary distribution determined by the degree sequence."
        />
      </section>
    </div>
  );
}
