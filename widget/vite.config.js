import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import cssInjectedByJsPlugin from 'vite-plugin-css-injected-by-js'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    cssInjectedByJsPlugin(),
  ],
  build: {
    lib: {
      entry: 'src/main.jsx',
      name: 'CourseCompanion',
      fileName: 'coursecompanion-widget',
      formats: ['iife']  // Immediately Invoked Function Expression for browser
    },
    rollupOptions: {
      output: {
        assetFileNames: 'coursecompanion-widget.[ext]',
        // Don't externalize dependencies - bundle everything
        inlineDynamicImports: true,
      }
    },
    // Optimize bundle size
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: false,  // Keep console for now
        drop_debugger: true
      }
    },
    // CSS handling
    cssCodeSplit: false,
  },
  // Development server config
  server: {
    port: 5173,
    open: true
  },
  // Copy public assets
  publicDir: 'public',
  // Enable CSS inline imports
  assetsInlineLimit: 0,
})