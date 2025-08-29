import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'  // ✅ This pulls in Tailwind (as long as index.css has the @tailwind directives)
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <App />
    </StrictMode>,
)
