export type Visibility = "public" | "followers" | "private";

export interface ArtifactMeta {
  glbUrl: string;
  usdzUrl: string;
  previewUrl: string;
  quality: {
    psnr: number;
    ssim: number;
    completeness: number;
  };
}

export interface JobStatus {
  id: string;
  status: "queued" | "processing" | "succeeded" | "failed";
  progress: number;
  artifacts?: ArtifactMeta;
  error?: string;
}

export interface FeedPost {
  id: string;
  ownerId: string;
  ownerName: string;
  caption: string;
  tags: string[];
  visibility: Visibility;
  createdAt: string;
  artifact: ArtifactMeta;
  likes: number;
  comments: number;
  hasLiked?: boolean;
}
