"use client";

import useSWR from "swr";
import { FeedPost } from "@fashion3d/types";
import { FeedCard } from "@/components/FeedCard";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function FeedPage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const { data, error, isLoading } = useSWR<FeedPost[]>(`${apiBase}/feed`, fetcher, {
    refreshInterval: 10000
  });

  if (error) {
    return <p className="text-rose-300">Failed to load feed.</p>;
  }

  if (isLoading || !data) {
    return <p className="text-slate-400">Loading runway magic...</p>;
  }

  return (
    <div className="grid gap-6">
      {data.map((post) => (
        <FeedCard key={post.id} post={post} />
      ))}
    </div>
  );
}
