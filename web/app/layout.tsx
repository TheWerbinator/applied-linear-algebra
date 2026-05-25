import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Applied Linear Algebra",
  description:
    "Six applied linear-algebra algorithms — k-means, Fourier fit, Hill cipher, AR forecast, Lotka-Volterra, random walk — as a typed FastAPI + Next.js demo.",
};

const NAV = [
  { href: "/clustering", label: "Clustering" },
  { href: "/fourier", label: "Fourier" },
  { href: "/hill-cipher", label: "Hill cipher" },
  { href: "/autoregressive", label: "AR forecast" },
  { href: "/lotka-volterra", label: "Lotka-Volterra" },
  { href: "/random-walk", label: "Random walk" },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-border bg-panel">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <Link href="/" className="font-mono text-lg font-semibold text-accent">
              applied-linear-algebra
            </Link>
            <nav className="hidden gap-4 md:flex">
              {NAV.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="text-sm text-gray-300 hover:text-accent"
                >
                  {item.label}
                </Link>
              ))}
            </nav>
            <a
              href="https://github.com/TheWerbinator/applied-linear-algebra"
              target="_blank"
              rel="noreferrer"
              className="text-xs text-gray-400 hover:text-accent"
            >
              github
            </a>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-10">{children}</main>
        <footer className="mt-16 border-t border-border py-6">
          <div className="mx-auto max-w-6xl px-6 text-xs text-gray-500">
            MIT licensed · numpy + FastAPI + Next.js · backend on Fly.io,
            frontend on Vercel
          </div>
        </footer>
      </body>
    </html>
  );
}
