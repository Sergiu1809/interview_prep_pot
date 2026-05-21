import { Outlet, Navigate, useNavigate, Link } from "react-router-dom"
 
function AuthGuard() {
    const navigate = useNavigate()
    const token = localStorage.getItem("token")
 
    if (!token) return <Navigate to="/" />
 
    return (
        <div className="app-layout">
            <header className="app-header">
                <Link to="/dashboard" className="app-logo">
                    Prep<span>AI</span>
                </Link>
                <nav className="app-nav">
                    <Link to="/dashboard">Dashboard</Link>
                    <Link to="/history">History</Link>
                    <button
                        className="btn btn-logout"
                        onClick={() => {
                            localStorage.removeItem("token")
                            navigate("/")
                        }}
                    >
                        Log out
                    </button>
                </nav>
            </header>
            <main className="app-main">
                <Outlet />
            </main>
        </div>
    )
}
 
export default AuthGuard