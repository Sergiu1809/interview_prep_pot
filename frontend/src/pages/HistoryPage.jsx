import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { apiRequest } from "../api"
 
function HistoryPage() {
    const [data, setData] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")
    const navigate = useNavigate()
 
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await apiRequest("/sessions/history/", "GET")
                const data = await response.json()
 
                if (response.ok) {
                    setData(data)
                }
            } catch {
                setError("Cannot connect to server")
            } finally {
                setLoading(false)
            }
        }
 
        fetchData()
    }, [])
 
    if (loading) return <div className="loading-page">Loading sessions...</div>
    if (error) return <div className="loading-page">{error}</div>
 
    return (
        <div>
            <div className="history-header">
                <h1>Session History</h1>
            </div>
 
            {data.length === 0 ? (
                <div className="empty-state">
                    <p>No sessions yet. Start your first interview!</p>
                    <button
                        className="btn btn-primary"
                        style={{ width: "auto", display: "inline-flex" }}
                        onClick={() => navigate("/dashboard")}
                    >
                        Go to Dashboard
                    </button>
                </div>
            ) : (
                <div className="session-list">
                    {data.map(session => (
                        <Link
                            to={`/history/${session.id}`}
                            key={session.id}
                            className="session-card"
                        >
                            <div className="session-card-left">
                                <h3>{session.topic || "Untitled Session"}</h3>
                                <div className="session-meta">
                                    <span className={`status-badge ${session.status}`}>
                                        {session.status}
                                    </span>
                                    <span>{session.total_questions} questions</span>
                                </div>
                            </div>
                            <div className="session-card-right">
                                <div className="session-score">
                                    {session.average_score > 0
                                        ? session.average_score
                                        : "—"}
                                </div>
                                <div className="session-score-label">avg score</div>
                            </div>
                        </Link>
                    ))}
                </div>
            )}
        </div>
    )
}
 
export default HistoryPage