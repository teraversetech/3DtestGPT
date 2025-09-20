import "./globals.css";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Fashion3D",
  description: "Capture, generate and share 3D fashion looks"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-50">
        <header className="border-b border-white/10 bg-slate-900/50 backdrop-blur">
          <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <Link href="/feed" className="text-lg font-semibold">
              Fashion3D
            </Link>
            <div className="flex items-center space-x-3 text-sm text-white/70">
              <Link href="/feed">Feed</Link>
              <Link href="/login">Login</Link>
            </div>
          </nav>
        </header>
        <main className="mx-auto min-h-screen max-w-6xl px-6 py-10">{children}</main>
      </body>
    </html>
  );
}
