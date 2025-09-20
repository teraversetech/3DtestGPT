import { useEffect, useRef, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Alert } from "react-native";
import { Camera, CameraType } from "expo-camera";
import * as FileSystem from "expo-file-system";
import { Buffer } from "buffer";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "expo-router";

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "http://localhost:8000";
const CHUNK_SIZE = Number(process.env.EXPO_PUBLIC_CHUNK_SIZE ?? 10 * 1024 * 1024);

export default function CaptureScreen() {
  const cameraRef = useRef<Camera | null>(null);
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const [recording, setRecording] = useState(false);
  const [progress, setProgress] = useState(0);
  const router = useRouter();

  useEffect(() => {
    if (!permission) {
      requestPermission();
    }
  }, [permission]);

  async function startRecording() {
    if (!cameraRef.current) return;
    try {
      setRecording(true);
      const video = await cameraRef.current.recordAsync({ maxDuration: 30, quality: "720p" });
      setRecording(false);
      await handleUpload(video.uri);
    } catch (error) {
      setRecording(false);
      Alert.alert("Capture error", String(error));
    }
  }

  function stopRecording() {
    cameraRef.current?.stopRecording();
  }

  async function handleUpload(uri: string) {
    // TODO: Face blur + EXIF stripping before upload using MediaPipe + ffmpeg
    const token = await AsyncStorage.getItem("token");
    if (!token) {
      Alert.alert("Not authenticated");
      return;
    }
    const info = await FileSystem.getInfoAsync(uri, { size: true });
    const init = await fetch(`${API_BASE}/uploads/init`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ filename: "capture.mp4", filesize: info.size ?? 0, content_type: "video/mp4" })
    });
    if (!init.ok) {
      Alert.alert("Upload failed", await init.text());
      return;
    }
    const initData = await init.json();
    const uploadId = initData.upload_id;

    const file = await FileSystem.readAsStringAsync(uri, { encoding: FileSystem.EncodingType.Base64 });
    const buffer = Buffer.from(file, "base64");
    const totalParts = Math.ceil(buffer.length / CHUNK_SIZE);
    const uploadedParts: number[] = [];
    for (let i = 0; i < totalParts; i += 1) {
      const chunk = buffer.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);
      const tempUri = `${FileSystem.cacheDirectory}chunk-${i + 1}.mp4`;
      await FileSystem.writeAsStringAsync(tempUri, chunk.toString("base64"), { encoding: FileSystem.EncodingType.Base64 });
      const form = new FormData();
      form.append("file", {
        uri: tempUri,
        name: `chunk-${i + 1}.mp4`,
        type: "video/mp4"
      } as any);
      const response = await fetch(`${API_BASE}/uploads/${uploadId}/part?part_number=${i + 1}`, {
        method: "PUT",
        headers: { Authorization: `Bearer ${token}` },
        body: form
      });
      await FileSystem.deleteAsync(tempUri, { idempotent: true });
      if (!response.ok) {
        Alert.alert("Chunk upload failed", await response.text());
        return;
      }
      uploadedParts.push(i + 1);
      setProgress(((i + 1) / totalParts) * 100);
    }

    await fetch(`${API_BASE}/uploads/${uploadId}/complete`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ parts: uploadedParts })
    });

    router.push({ pathname: "/upload", params: { uploadId } });
  }

  return (
    <View style={styles.container}>
      {permission?.granted ? (
        <Camera style={styles.camera} type={CameraType.back} ref={(ref) => (cameraRef.current = ref)}>
          <View style={styles.guide}>
            <View style={styles.ring} />
            <Text style={styles.instructions}>Orbit around the look. Keep the guide centered.</Text>
          </View>
        </Camera>
      ) : (
        <Text style={styles.instructions}>Camera permission required.</Text>
      )}
      <View style={styles.actions}>
        {recording ? (
          <TouchableOpacity style={styles.stopButton} onPress={stopRecording}>
            <Text style={styles.buttonText}>Stop</Text>
          </TouchableOpacity>
        ) : (
          <TouchableOpacity style={styles.recordButton} onPress={startRecording}>
            <Text style={styles.buttonText}>Record</Text>
          </TouchableOpacity>
        )}
        {progress > 0 ? (
          <View style={styles.progressBar}>
            <View style={[styles.progressFill, { width: `${progress}%` }]} />
          </View>
        ) : null}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "black" },
  camera: { flex: 1 },
  actions: {
    padding: 24,
    backgroundColor: "#020617"
  },
  recordButton: {
    backgroundColor: "#22c55e",
    padding: 18,
    borderRadius: 999,
    alignItems: "center"
  },
  stopButton: {
    backgroundColor: "#ef4444",
    padding: 18,
    borderRadius: 999,
    alignItems: "center"
  },
  buttonText: {
    color: "white",
    fontWeight: "700"
  },
  guide: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center"
  },
  ring: {
    width: 240,
    height: 240,
    borderRadius: 120,
    borderWidth: 4,
    borderColor: "rgba(255,255,255,0.6)"
  },
  instructions: {
    textAlign: "center",
    color: "white",
    marginTop: 16,
    paddingHorizontal: 24
  },
  progressBar: {
    height: 8,
    marginTop: 16,
    backgroundColor: "rgba(255,255,255,0.2)",
    borderRadius: 4
  },
  progressFill: {
    height: 8,
    backgroundColor: "#38bdf8",
    borderRadius: 4
  }
});
