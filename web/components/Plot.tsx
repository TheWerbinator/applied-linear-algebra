"use client";

import dynamic from "next/dynamic";
import type { Data, Layout } from "plotly.js-dist-min";

const Plotly = dynamic(() => import("react-plotly.js"), {
  ssr: false,
  loading: () => (
    <div className="flex h-96 items-center justify-center rounded border border-border bg-panel text-sm text-gray-400">
      loading plot…
    </div>
  ),
});

interface Props {
  data: Data[];
  layout?: Partial<Layout>;
  className?: string;
}

const DEFAULT_LAYOUT: Partial<Layout> = {
  paper_bgcolor: "#111827",
  plot_bgcolor: "#0b0f17",
  font: { color: "#e5e7eb", family: "ui-sans-serif, system-ui" },
  margin: { t: 40, r: 20, b: 50, l: 60 },
  xaxis: { gridcolor: "#1f2937", zerolinecolor: "#374151" },
  yaxis: { gridcolor: "#1f2937", zerolinecolor: "#374151" },
  autosize: true,
};

export default function Plot({ data, layout, className }: Props) {
  const mergedLayout: Partial<Layout> = { ...DEFAULT_LAYOUT, ...layout };
  return (
    <div className={className ?? "h-96 w-full"}>
      <Plotly
        data={data}
        layout={mergedLayout}
        config={{ responsive: true, displaylogo: false }}
        useResizeHandler
        style={{ width: "100%", height: "100%" }}
      />
    </div>
  );
}
