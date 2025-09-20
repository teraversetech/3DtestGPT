"use client";

import { useState } from "react";
import { Button, Card, CardContent, CardHeader } from "@fashion3d/ui";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const apiBase = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
    const response = await fetch(`${apiBase}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (!response.ok) {
      setMessage("Invalid credentials");
      return;
    }
    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    setMessage("Logged in! Redirecting...");
  }

  return (
    <div className="mx-auto max-w-md">
      <Card>
        <CardHeader>
          <h1 className="text-2xl font-semibold">Welcome back</h1>
          <p className="text-sm text-slate-500">Scan looks, share splats, earn fans.</p>
        </CardHeader>
        <CardContent>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <label className="block text-sm font-medium">
              Email
              <input
                className="mt-1 w-full rounded-md border border-slate-200 bg-slate-950 px-3 py-2 text-slate-100"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                type="email"
                required
              />
            </label>
            <label className="block text-sm font-medium">
              Password
              <input
                className="mt-1 w-full rounded-md border border-slate-200 bg-slate-950 px-3 py-2 text-slate-100"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                type="password"
                required
              />
            </label>
            <Button type="submit" className="w-full">
              Sign in
            </Button>
            {message ? <p className="text-sm text-emerald-400">{message}</p> : null}
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
