"use client";

import { useState } from "react";
import AlgoLayout from "@/components/AlgoLayout";
import { api } from "@/lib/api";
import type { HillEncryptResponse } from "@/lib/types";

export default function HillCipherPage() {
  const [plaintext, setPlaintext] = useState("linear algebra is great");
  const [blockSize, setBlockSize] = useState(3);
  const [seed, setSeed] = useState(0);
  const [result, setResult] = useState<HillEncryptResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.hillEncrypt({ plaintext, block_size: blockSize, seed });
      setResult(r);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AlgoLayout
      title="Hill cipher (modular)"
      subtitle="Cryptography · modular linear algebra"
      description={
        "Classical block cipher: encrypt c = (A m + b) mod p, decrypt m = A⁻¹ (c - b) mod p. The matrix inverse is computed in Z_p via Fermat's little theorem rather than over the reals — round-tripping is exact for any prime modulus and any invertible A."
      }
      controls={
        <div className="space-y-3">
          <div>
            <label htmlFor="text">Plaintext</label>
            <textarea
              id="text"
              rows={3}
              value={plaintext}
              onChange={(e) => setPlaintext(e.target.value)}
              className="mt-1 w-full font-mono"
            />
          </div>
          <div>
            <label htmlFor="bs">Block size</label>
            <input
              id="bs"
              type="number"
              min={2}
              max={6}
              value={blockSize}
              onChange={(e) => setBlockSize(Number(e.target.value))}
              className="mt-1 w-full"
            />
          </div>
          <div>
            <label htmlFor="seed">Key seed</label>
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
            {loading ? "Encrypting…" : "Encrypt"}
          </button>
          {error && <p className="text-xs text-red-400">{error}</p>}
        </div>
      }
      visualization={
        result ? (
          <div className="space-y-4 text-sm">
            <Field label="Plaintext" value={result.plaintext} />
            <Field
              label={`Ciphertext blocks (mod ${result.modulus})`}
              value={result.ciphertext
                .map((row) => `[${row.join(", ")}]`)
                .join("\n")}
            />
            <Field label="Decrypted (round-trip)" value={result.decrypted} />
            <div className="grid gap-3 md:grid-cols-2">
              <Field
                label="Key matrix A"
                value={result.key_A.map((row) => row.join("\t")).join("\n")}
              />
              <Field label="Key vector b" value={result.key_b.join(", ")} />
            </div>
            <div className="rounded border border-border bg-background p-3 text-sm">
              Round trip:{" "}
              <span
                className={result.round_trip_ok ? "text-emerald-400" : "text-red-400"}
              >
                {result.round_trip_ok ? "OK" : "FAILED"}
              </span>
            </div>
          </div>
        ) : (
          <div className="flex h-96 items-center justify-center text-sm text-gray-500">
            Enter plaintext and encrypt.
          </div>
        )
      }
    />
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="mb-1 text-xs uppercase tracking-wide text-gray-500">{label}</div>
      <pre className="overflow-x-auto whitespace-pre-wrap break-words rounded border border-border bg-background p-3 font-mono text-xs text-gray-200">
        {value}
      </pre>
    </div>
  );
}
