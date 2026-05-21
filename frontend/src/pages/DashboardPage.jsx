import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { apiRequest } from "../api"
 
function DashboardPage() {
    const [topic, setTopic] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
 
    const navigate = useNavigate()
 
    const createSession = async () => {
        if (!topic.trim()) {
            setError("Please enter a topic")
            return
        }
 
        if (loading) return
        setLoading(true)
        setError("")
 
        try {
            const response = await apiRequest("/sessions/", "POST", { topic: topic })
 
            const data = await response.json()
 
            if (response.ok) {
                navigate(`/interview/${data.id}`)
            } else {
                if (typeof data.detail === "string") {
                    setError(data.detail)
                } else {
                    setError("Please enter a topic")
                }
            }
        } catch (err) {
            setError("Cannot connect to server")
        } finally {
            setLoading(false)
        }
    }
 
    return (
        <div>
            <div className="dashboard-header">
                <h1>Dashboard</h1>
                <p>Start a new interview session or review past ones.</p>
            </div>
 
            <div className="dashboard-new-session">
                <h2>New Session</h2>
                <div className="input-row">
                    <input
                        type="text"
                        placeholder="Enter a topic (e.g. Python, SQL, System Design)"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                    />
                    <button
                        className="btn btn-primary"
                        onClick={createSession}
                        disabled={loading}
                    >
                        {loading ? "Creating..." : "Start"}
                    </button>
                </div>
                {error && <p className="error-msg">{error}</p>}
            </div>
        </div>
    )
}
 
export default DashboardPage