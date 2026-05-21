import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { apiRequest } from "../api"
 
function RegisterPage() {
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
 
    const navigate = useNavigate()
 
    const handleRegister = async () => {
        if (!name.trim()) {
            setError("Please enter your name")
            return
        }
        if (!email.trim()) {
            setError("Please enter your email")
            return
        }
        if (password.length < 8) {
            setError("Password must be at least 8 characters")
            return
        }
 
        if (loading) return
        setLoading(true)
        setError("")
 
        try {
            const response = await apiRequest("/auth/register", "POST", {
                name: name,
                email: email,
                password: password
            })
 
            const data = await response.json()
 
            if (response.ok) {
                navigate("/")
            } else {
                if (typeof data.detail === "string") {
                    setError(data.detail)
                } else {
                    setError("All fields are mandatory")
                }
            }
        } catch (err) {
            setError("Cannot connect to server")
        } finally {
            setLoading(false)
        }
    }
 
    return (
        <div className="auth-wrapper">
            <div className="auth-card">
                <h1>Create account</h1>
                <p className="auth-subtitle">Start preparing for your next interview</p>
                <div className="auth-fields">
                    <input
                        type="text"
                        placeholder="Full name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    <input
                        type="email"
                        placeholder="Email address"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password (min 8 characters)"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button
                    className="btn btn-primary"
                    onClick={handleRegister}
                    disabled={loading}
                >
                    {loading ? "Creating account..." : "Create account"}
                </button>
                {error && <p className="error-msg">{error}</p>}
                <p className="auth-footer">
                    Already have an account? <Link to="/">Sign in</Link>
                </p>
            </div>
        </div>
    )
}
 
export default RegisterPage