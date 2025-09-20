#!/usr/bin/env node
const { spawnSync } = require("node:child_process");
const path = require("node:path");

const jestBin = require.resolve("jest/bin/jest");
const cliArgs = process.argv.slice(2).filter((arg) => arg !== "--");

const result = spawnSync(process.execPath, [jestBin, ...cliArgs], {
  stdio: "inherit",
  cwd: path.resolve(__dirname, "..")
});

if (result.error) {
  console.error(result.error);
  process.exit(1);
}
process.exit(result.status ?? 1);
