import { Link, Redirect } from "expo-router";
import { useEffect, useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "http://localhost:8000";

export default function AuthScreen() {
  const [email, setEmail] = useState("demo@fashion3d.dev");
  const [password, setPassword] = useState("password");
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    AsyncStorage.getItem("token").then(setToken);
  }, []);

  if (token) {
    return <Redirect href="/feed" />;
  }

  async function handleLogin() {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (!response.ok) {
      Alert.alert("Login failed", "Check your credentials");
      return;
    }
    const data = await response.json();
    await AsyncStorage.setItem("token", data.access_token);
    setToken(data.access_token);
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Fashion3D</Text>
      <Text style={styles.subtitle}>Capture. Generate. Share.</Text>
      <TextInput
        style={styles.input}
        placeholder="Email"
        placeholderTextColor="#94a3b8"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        placeholderTextColor="#94a3b8"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Sign in</Text>
      </TouchableOpacity>
      <Text style={styles.disclaimer}>
        By continuing you agree to our Terms & Privacy. TODO: present modals for explicit consent.
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#020617",
    alignItems: "center",
    justifyContent: "center",
    padding: 24
  },
  title: {
    fontSize: 32,
    fontWeight: "700",
    color: "white"
  },
  subtitle: {
    color: "#64748b",
    marginBottom: 24
  },
  input: {
    width: "100%",
    borderRadius: 12,
    padding: 16,
    backgroundColor: "#0f172a",
    color: "white",
    marginBottom: 12
  },
  button: {
    backgroundColor: "#2563eb",
    padding: 16,
    borderRadius: 12,
    width: "100%",
    alignItems: "center"
  },
  buttonText: {
    color: "white",
    fontWeight: "600"
  },
  disclaimer: {
    color: "#64748b",
    fontSize: 12,
    textAlign: "center",
    marginTop: 16
  }
});
