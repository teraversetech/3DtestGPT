import { render, screen } from "@testing-library/react";
import { FeedCard } from "@/components/FeedCard";
import { FeedPost } from "@fashion3d/types";

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
    render(<FeedCard post={mockPost} />);
    expect(screen.getByText(/Holographic trench coat/i)).toBeInTheDocument();
    expect(screen.getByText(/#hologram/i)).toBeInTheDocument();
  });
});
