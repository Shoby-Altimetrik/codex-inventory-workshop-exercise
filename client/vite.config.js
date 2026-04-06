import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'jsdom',
    exclude: [
      '**/node_modules/**',
      '**/node_modules.bak*/**',
      '**/dist/**',
      '**/coverage/**'
    ]
  }
})
