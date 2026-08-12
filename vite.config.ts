import { defineConfig, type UserConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

const replitPlugins = async () => {
  if (!process.env.REPL_ID) return [];
  const [cartographer, devBanner, runtimeErrorModal] = await Promise.all([
    import("@replit/vite-plugin-cartographer").then((m) => m.cartographer()),
    import("@replit/vite-plugin-dev-banner").then((m) => m.devBanner()),
    import("@replit/vite-plugin-runtime-error-modal").then((m) => m.default()),
  ]);
  return [cartographer, devBanner, runtimeErrorModal];
};

export default defineConfig(async (): Promise<UserConfig> => ({
  root: path.resolve(import.meta.dirname, "client"),
  plugins: [react(), tailwindcss(), ...(await replitPlugins())],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
      "@shared": path.resolve(import.meta.dirname, "shared"),
    },
  },
  build: {
    outDir: path.resolve(import.meta.dirname, "dist", "public"),
    emptyOutDir: true,
  },
  server: {
    host: "0.0.0.0",
    port: 5000,
    allowedHosts: true,
  },
}));
