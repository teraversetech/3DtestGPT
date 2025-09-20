import { useLocalSearchParams } from "expo-router";
import { useEffect, useState } from "react";
import { View, Text, StyleSheet, ScrollView, Image } from "react-native";

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "http://localhost:8000";

type PostDetail = {
  id: string;
  caption: string;
  ownerName: string;
  likes: number;
  artifact: { previewUrl: string };
};

export default function PostDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [post, setPost] = useState<PostDetail | null>(null);

  useEffect(() => {
    async function fetchPost() {
      const response = await fetch(`${API_BASE}/feed`);
      const data = await response.json();
      const match = data.find((item: PostDetail) => item.id === id);
      setPost(match ?? null);
    }
    fetchPost();
  }, [id]);

  if (!post) {
    return (
      <View style={styles.container}>
        <Text style={styles.loading}>Loading…</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.author}>{post.ownerName}</Text>
      <Text style={styles.caption}>{post.caption}</Text>
      <Image source={{ uri: post.artifact.previewUrl }} style={styles.preview} />
      <Text style={styles.meta}>❤️ {post.likes} likes</Text>
      <Text style={styles.todo}>TODO: embed interactive 3D viewer via expo-three</Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: "#020617",
    padding: 24
  },
  loading: {
    color: "white"
  },
  author: {
    color: "#38bdf8",
    fontWeight: "600",
    fontSize: 18
  },
  caption: {
    color: "white",
    marginTop: 12
  },
  preview: {
    width: "100%",
    height: 240,
    borderRadius: 16,
    marginTop: 16
  },
  meta: {
    color: "#94a3b8",
    marginTop: 12
  },
  todo: {
    color: "#fbbf24",
    marginTop: 24
  }
});
