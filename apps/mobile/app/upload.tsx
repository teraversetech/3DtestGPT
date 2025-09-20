import { useLocalSearchParams, useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { View, Text, StyleSheet, ActivityIndicator, Alert, TouchableOpacity } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "http://localhost:8000";

interface JobStatus {
  id: string;
  status: string;
  progress: number;
}

export default function UploadProgressScreen() {
  const { uploadId } = useLocalSearchParams<{ uploadId: string }>();
  const [job, setJob] = useState<JobStatus | null>(null);
  const router = useRouter();

  useEffect(() => {
    async function createJob() {
      const token = await AsyncStorage.getItem("token");
      if (!token) return;
      const response = await fetch(`${API_BASE}/jobs`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify({ upload_id: uploadId })
      });
      if (!response.ok) {
        Alert.alert("Job creation failed", await response.text());
        return;
      }
      const data = await response.json();
      pollJob(token, data.id);
    }
    createJob();
  }, [uploadId]);

  async function pollJob(token: string, jobId: string) {
    const interval = setInterval(async () => {
      const response = await fetch(`${API_BASE}/jobs/${jobId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!response.ok) return;
      const data = await response.json();
      setJob(data);
      if (data.status === "succeeded") {
        clearInterval(interval);
        Alert.alert("Ready!", "Your 3D look is live.");
        router.replace(`/feed`);
      }
    }, 8000);
  }

  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#22d3ee" />
      <Text style={styles.title}>Generating splats and meshes…</Text>
      <Text style={styles.subtitle}>Status: {job?.status ?? "queued"}</Text>
      <Text style={styles.subtitle}>Progress: {job?.progress ?? 0}%</Text>
      <TouchableOpacity style={styles.button} onPress={() => router.replace("/feed")}>
        <Text style={styles.buttonText}>Back to feed</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#020617",
    padding: 24
  },
  title: {
    marginTop: 24,
    fontSize: 24,
    fontWeight: "700",
    color: "white"
  },
  subtitle: {
    color: "#94a3b8",
    marginTop: 8
  },
  button: {
    marginTop: 32,
    backgroundColor: "#1d4ed8",
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 999
  },
  buttonText: {
    color: "white",
    fontWeight: "600"
  }
});
