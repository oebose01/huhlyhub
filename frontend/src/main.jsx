import React from 'react'
import ReactDOM from 'react-dom/client'
import * as Sentry from "@sentry/react"
import App from './App'
import './index.css'

Sentry.init({
  dsn: "YOUR_REACT_DSN", // Replace with your actual Sentry DSN
  integrations: [Sentry.browserTracingIntegration()],
  tracesSampleRate: 1.0,
  environment: import.meta.env.MODE,
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
