import { notFound } from "next/navigation";
import { FeedCard } from "@/components/FeedCard";
import { FeedPost } from "@fashion3d/types";

async function fetchPost(id: string): Promise<FeedPost | null> {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const response = await fetch(`${apiBase}/feed`);
  if (!response.ok) return null;
  const posts: FeedPost[] = await response.json();
  return posts.find((post) => post.id === id) ?? null;
}

export default async function PostDetail({ params }: { params: { id: string } }) {
  const post = await fetchPost(params.id);
  if (!post) {
    notFound();
  }
  return (
    <div className="space-y-6">
      <FeedCard post={post} />
      <section className="rounded-xl border border-white/10 bg-slate-900/60 p-6">
        <h3 className="text-lg font-semibold">Social reactions</h3>
        <p className="text-sm text-slate-400">Likes: {post.likes} · Comments: {post.comments}</p>
        <p className="text-sm text-slate-500">
          TODO: Render live comment thread, commerce hooks, and AR try-on CTA.
        </p>
      </section>
    </div>
  );
}
