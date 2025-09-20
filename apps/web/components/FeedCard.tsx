import Link from "next/link";
import Image from "next/image";
import { FeedPost } from "@fashion3d/types";
import { Card, CardContent, CardHeader, CardFooter, Button } from "@fashion3d/ui";
import { ThreeViewer } from "./ThreeViewer";

interface FeedCardProps {
  post: FeedPost;
}

export function FeedCard({ post }: FeedCardProps) {
  return (
    <Card className="overflow-hidden border-white/10 bg-slate-900/60">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold">{post.ownerName}</h2>
            <p className="text-sm text-slate-400">{new Date(post.createdAt).toLocaleString()}</p>
          </div>
          <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-xs uppercase text-emerald-300">
            {post.visibility}
          </span>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <p>{post.caption}</p>
        <div className="overflow-hidden rounded-xl border border-white/5 bg-slate-950/40">
          <ThreeViewer src={post.artifact.glbUrl} poster={post.artifact.previewUrl} />
        </div>
        <div className="flex flex-wrap gap-2 text-xs uppercase tracking-wider text-slate-400">
          {post.tags.map((tag) => (
            <span key={tag} className="rounded-full bg-white/10 px-2 py-1">
              #{tag}
            </span>
          ))}
        </div>
      </CardContent>
      <CardFooter className="justify-between text-sm text-slate-400">
        <span>❤️ {post.likes}</span>
        <span>💬 {post.comments}</span>
        <Link href={`/post/${post.id}`}>Open</Link>
      </CardFooter>
    </Card>
  );
}
