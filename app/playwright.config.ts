import { fileURLToPath } from "node:url";

import { defineConfig } from "@playwright/test";

/** O e2e roda contra o servidor de verdade (`curso web`), sem mock nenhum. */
export default defineConfig({
  testDir: fileURLToPath(new URL("./e2e", import.meta.url)),
  timeout: 60_000,
  fullyParallel: false,
  workers: 1,
  retries: 0,
  use: {
    baseURL: "http://127.0.0.1:8765",
    launchOptions: { executablePath: "/opt/pw-browsers/chromium" },
  },
});
