import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// The proxy target is development configuration, not an application contract.
// It can be changed per machine without editing source code.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiTarget = env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000'

  return {
    plugins: [react()],
    server: {
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
        },
      },
    },
  }
})
