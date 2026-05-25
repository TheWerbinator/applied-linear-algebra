import Link from "next/link";
import type { Route } from "next";

interface Props {
  href: Route;
  title: string;
  blurb: string;
  topic: string;
}

export default function AlgoCard({ href, title, blurb, topic }: Props) {
  return (
    <Link
      href={href}
      className="group block rounded-lg border border-border bg-panel p-5 transition hover:border-accent"
    >
      <div className="mb-2 text-xs uppercase tracking-wide text-gray-500">
        {topic}
      </div>
      <h3 className="mb-2 text-lg font-semibold text-gray-100 group-hover:text-accent">
        {title}
      </h3>
      <p className="text-sm text-gray-400">{blurb}</p>
    </Link>
  );
}
