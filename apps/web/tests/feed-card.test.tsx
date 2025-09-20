import { FeedCard } from "@/components/FeedCard";
import { FeedPost } from "@fashion3d/types";
import { renderToString } from "react-dom/server";

const mockPost: FeedPost = {
  id: "post-1",
  ownerId: "user-1",
  ownerName: "stylist@fashion3d.dev",
  caption: "Holographic trench coat",
  tags: ["hologram", "coat"],
  visibility: "public",
  createdAt: new Date().toISOString(),
  artifact: {
    glbUrl: "https://example.com/model.glb",
    usdzUrl: "https://example.com/model.usdz",
    previewUrl: "https://example.com/preview.jpg",
    quality: { psnr: 28, ssim: 0.9, completeness: 0.95 }
  },
  likes: 12,
  comments: 3,
  hasLiked: false
};

describe("FeedCard", () => {
  it("renders caption and tags", () => {
    const html = renderToString(<FeedCard post={mockPost} />);
    expect(html).toContain("Holographic trench coat");
    expect(html).toContain("#hologram");
  });
});
