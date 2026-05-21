import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
 
function LoginPage() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
 
    const navigate = useNavigate()
 
    const handleLogin = async () => {
        if (loading) return
        setLoading(true)
        setError("")
 
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ username: email, password: password })
            })
 
            const data = await response.json()
 
            if (response.ok) {
                localStorage.setItem("token", data.access_token)
                navigate("/dashboard")
            } else {
                if (typeof data.detail === "string") {
                    setError(data.detail)
                } else {
                    setError("Invalid email or password")
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
                <h1>Welcome back</h1>
                <p className="auth-subtitle">Sign in to continue your interview prep</p>
                <div className="auth-fields">
                    <input
                        type="email"
                        placeholder="Email address"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button
                    className="btn btn-primary"
                    onClick={handleLogin}
                    disabled={loading}
                >
                    {loading ? "Signing in..." : "Sign in"}
                </button>
                {error && <p className="error-msg">{error}</p>}
                <p className="auth-footer">
                    Don't have an account? <Link to="/register">Create one</Link>
                </p>
            </div>
        </div>
    )
}
 
export default LoginPage