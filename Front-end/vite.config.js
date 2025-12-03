// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react'

// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
// })

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // SPA fallback for React Router
    fs: {
      strict: false
    }
  },
  build: {
    rollupOptions: {
      input: 'index.html'
    }
  }
});
