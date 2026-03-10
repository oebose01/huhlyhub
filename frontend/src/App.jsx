import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ContentRegistration from './pages/ContentRegistration'
import Verify from './pages/Verify'
import Subscription from './pages/Subscription'

function App() {
  return (
    <Router>
      <AuthProvider>
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/register-content" element={<ContentRegistration />} />
            <Route path="/verify" element={<Verify />} />
            <Route path="/subscription" element={<Subscription />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App
