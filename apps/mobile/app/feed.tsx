import { useFocusEffect, useRouter } from "expo-router";
import { useCallback, useState } from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity, RefreshControl } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "http://localhost:8000";

type ArtifactMeta = {
  preview_url: string;
  glb_url: string;
};

type FeedItem = {
  id: string;
  caption: string;
  ownerName: string;
  tags: string[];
  likes: number;
  artifact: { previewUrl: string; glbUrl: string };
};

export default function FeedScreen() {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const router = useRouter();

  async function loadFeed() {
    setRefreshing(true);
    const token = await AsyncStorage.getItem("token");
    const response = await fetch(`${API_BASE}/feed`, {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined
    });
    const data = await response.json();
    setItems(data);
    setRefreshing(false);
  }

  useFocusEffect(
    useCallback(() => {
      loadFeed();
    }, [])
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadFeed} />}
        contentContainerStyle={{ padding: 16, gap: 16 }}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.card}
            onPress={() => router.push({ pathname: `/post/${item.id}`, params: { id: item.id } })}
          >
            <Text style={styles.author}>{item.ownerName}</Text>
            <Text style={styles.caption}>{item.caption}</Text>
            <Text style={styles.meta}>❤️ {item.likes}</Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={<Text style={styles.empty}>No splats yet. Capture your first look!</Text>}
      />
      <TouchableOpacity style={styles.captureButton} onPress={() => router.push("/capture")}>
        <Text style={styles.captureText}>Capture</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#020617" },
  card: {
    backgroundColor: "#0f172a",
    padding: 16,
    borderRadius: 16
  },
  author: {
    color: "#38bdf8",
    fontWeight: "600"
  },
  caption: {
    color: "white",
    marginTop: 8
  },
  meta: {
    color: "#94a3b8",
    marginTop: 12
  },
  empty: {
    color: "#94a3b8",
    textAlign: "center",
    marginTop: 48
  },
  captureButton: {
    position: "absolute",
    bottom: 32,
    right: 24,
    backgroundColor: "#22c55e",
    paddingHorizontal: 24,
    paddingVertical: 16,
    borderRadius: 999
  },
  captureText: {
    color: "black",
    fontWeight: "700"
  }
});
