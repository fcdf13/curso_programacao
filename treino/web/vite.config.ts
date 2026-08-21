import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

// A API roda no uvicorn; em desenvolvimento o Vite repassa /api para lá, o que
// mantém tudo na mesma origem e faz o cookie de sessão funcionar sem CORS.
const API = "http://127.0.0.1:8770";

export default defineConfig({
  server: {
    port: 5180,
    proxy: { "/api": { target: API, changeOrigin: true } },
  },
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["apple-touch-icon.png", "favicon-32.png"],
      manifest: {
        name: "JF Treino",
        short_name: "JF Treino",
        description: "Acompanhamento de treino com o João Filho",
        lang: "pt-BR",
        start_url: "/",
        display: "standalone",
        orientation: "portrait",
        background_color: "#101010",
        theme_color: "#101010",
        icons: [
          { src: "icone-192.png", sizes: "192x192", type: "image/png" },
          { src: "icone-512.png", sizes: "512x512", type: "image/png" },
          {
            src: "icone-maskable-512.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
      workbox: {
        // A casca do app fica em cache; /api nunca, porque uma resposta velha de
        // /api/eu deixaria o app achando que tem alguém logado quando não tem.
        navigateFallbackDenylist: [/^\/api\//],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/fonts\.(googleapis|gstatic)\.com\//,
            handler: "CacheFirst",
            options: {
              cacheName: "fontes",
              expiration: { maxEntries: 12, maxAgeSeconds: 60 * 60 * 24 * 365 },
              cacheableResponse: { statuses: [0, 200] },
            },
          },
        ],
      },
    }),
  ],
});
