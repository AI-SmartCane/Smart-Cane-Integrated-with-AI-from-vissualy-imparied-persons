import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// GitHub Pages serves the site from https://naskenai.github.io/edge-vision-guidance-cane/
export default defineConfig({
  base: "/edge-vision-guidance-cane/",
  plugins: [react(), tailwindcss()],
  preview: {
    port: 4173,
    strictPort: true,
  },
});
