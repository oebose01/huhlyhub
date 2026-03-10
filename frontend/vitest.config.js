import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
    // Transform ES modules in extension and src
    transformMode: {
      web: [/\.[jt]sx?$/],
    },
    deps: {
      inline: ['http:', 'https:'],
    },
    server: {
      deps: {
        inline: ['http:', 'https:'],
      },
    },
  },
})
