#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const projectRoot = process.cwd();

function checkContains(relativePath, expectedSnippets) {
  const filePath = resolve(projectRoot, relativePath);
  const content = readFileSync(filePath, "utf-8");
  const missing = expectedSnippets.filter((snippet) => !content.includes(snippet));
  if (missing.length > 0) {
    throw new Error(
      `Expected ${relativePath} to include:\n${missing.map((s) => `  - ${s}`).join("\n")}\n`
    );
  }
}

function run() {
  checkContains("components/ThreeViewer.tsx", [
    "GLTFLoader",
    "HemisphereLight",
    'aria-label="3D preview"',
  ]);

  checkContains("components/FeedCard.tsx", [
    "ThreeViewer",
    "CardHeader",
    "#{tag}",
  ]);

  checkContains("app/(feed)/page.tsx", [
    "FeedCard",
    "useSWR",
  ]);

  checkContains("app/(auth)/login/page.tsx", [
    "Email",
    "Sign in",
  ]);

  console.log("✅ Offline smoke checks passed");
}

try {
  run();
} catch (error) {
  console.error("❌ Offline smoke checks failed");
  console.error(error.message || error);
  process.exit(1);
}
