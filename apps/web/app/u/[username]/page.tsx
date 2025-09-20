import { FeedCard } from "@/components/FeedCard";
import { FeedPost } from "@fashion3d/types";

async function fetchUserPosts(username: string): Promise<FeedPost[]> {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const response = await fetch(`${apiBase}/feed`);
  if (!response.ok) return [];
  const posts: FeedPost[] = await response.json();
  return posts.filter((post) => post.ownerName.split("@")[0] === username);
}

export default async function UserProfile({ params }: { params: { username: string } }) {
  const posts = await fetchUserPosts(params.username);
  return (
    <div className="space-y-6">
      <header className="rounded-xl border border-white/10 bg-slate-900/60 p-6">
        <h1 className="text-2xl font-semibold">@{params.username}</h1>
        <p className="text-sm text-slate-400">Showcasing splats, meshes, and looks.</p>
      </header>
      <div className="grid gap-6">
        {posts.map((post) => (
          <FeedCard key={post.id} post={post} />
        ))}
      </div>
    </div>
  );
}
