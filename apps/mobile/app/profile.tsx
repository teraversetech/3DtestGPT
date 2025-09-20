import { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "expo-router";

export default function ProfileScreen() {
  const [email, setEmail] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    AsyncStorage.getItem("token");
    setEmail("demo@fashion3d.dev");
  }, []);

  async function handleLogout() {
    await AsyncStorage.removeItem("token");
    router.replace("/");
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Profile</Text>
      <Text style={styles.subtitle}>Plan: Pro (trial)</Text>
      <Text style={styles.subtitle}>Email: {email}</Text>
      <TouchableOpacity style={styles.button} onPress={handleLogout}>
        <Text style={styles.buttonText}>Sign out</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#020617",
    gap: 12
  },
  title: {
    fontSize: 24,
    fontWeight: "700",
    color: "white"
  },
  subtitle: {
    color: "#94a3b8"
  },
  button: {
    marginTop: 16,
    backgroundColor: "#ef4444",
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 999
  },
  buttonText: {
    color: "white",
    fontWeight: "600"
  }
});
