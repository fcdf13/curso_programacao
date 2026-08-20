import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// `root` e `outDir` saem da localização deste arquivo, não do diretório de onde
// o comando foi chamado — assim `npm run build` sempre produz app/dist, esteja
// você na raiz do repositório ou dentro de app/.
export default defineConfig({
  root: fileURLToPath(new URL(".", import.meta.url)),
  plugins: [react()],
  server: {
    port: 5173,
    // Em desenvolvimento o Vite serve o front e repassa /api ao backend Python:
    // o navegador só conhece uma origem, e não há CORS para configurar.
    proxy: { "/api": "http://127.0.0.1:8765" },
  },
  build: {
    outDir: fileURLToPath(new URL("./dist", import.meta.url)),
    emptyOutDir: true,
    sourcemap: false,
  },
});
