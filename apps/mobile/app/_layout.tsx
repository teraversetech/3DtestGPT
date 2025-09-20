import { Stack } from "expo-router";
import { useEffect } from "react";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import { Buffer } from "buffer";

(global as any).Buffer = (global as any).Buffer ?? Buffer;

export default function RootLayout() {
  useEffect(() => {
    // TODO: configure push notifications + permissions
  }, []);

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <StatusBar style="light" />
        <Stack screenOptions={{ headerShown: false }}>
          <Stack.Screen name="index" />
          <Stack.Screen name="capture" />
          <Stack.Screen name="upload" />
          <Stack.Screen name="feed" />
          <Stack.Screen name="post/[id]" />
          <Stack.Screen name="profile" />
        </Stack>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}
