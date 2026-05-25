interface Props {
  title: string;
  subtitle: string;
  description: string;
  controls: React.ReactNode;
  visualization: React.ReactNode;
  details?: React.ReactNode;
}

export default function AlgoLayout({
  title,
  subtitle,
  description,
  controls,
  visualization,
  details,
}: Props) {
  return (
    <div className="space-y-6">
      <header>
        <p className="text-xs uppercase tracking-wide text-gray-500">{subtitle}</p>
        <h1 className="mt-1 text-3xl font-semibold text-gray-100">{title}</h1>
        <p className="mt-3 max-w-3xl text-sm leading-relaxed text-gray-400">
          {description}
        </p>
      </header>
      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        <aside className="space-y-4 rounded-lg border border-border bg-panel p-5">
          <h2 className="text-xs font-semibold uppercase tracking-wide text-gray-500">
            Parameters
          </h2>
          {controls}
        </aside>
        <section className="rounded-lg border border-border bg-panel p-5">
          {visualization}
        </section>
      </div>
      {details && (
        <section className="rounded-lg border border-border bg-panel p-5 text-sm text-gray-300">
          {details}
        </section>
      )}
    </div>
  );
}
