import { useState, useEffect } from "react"
import { useParams, Link } from "react-router-dom"
import { apiRequest } from "../api"
 
function SessionDetailPage() {
    const { sessionId } = useParams()
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState({})
    const [error, setError] = useState("")
 
    const getScoreClass = (score) => {
        if (score >= 7) return "high"
        if (score >= 4) return "mid"
        return "low"
    }
 
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await apiRequest(`/sessions/history/${sessionId}`, "GET")
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
 
    if (loading) return <div className="loading-page">Loading session...</div>
    if (error) return <div className="loading-page">{error}</div>
 
    return (
        <div>
            <div className="detail-header">
                <Link to="/history" className="btn btn-ghost">← Back to History</Link>
                <h1>{data.topic}</h1>
                <div className="detail-meta">
                    <span className={`status-badge ${data.status}`}>{data.status}</span>
                    <span>{data.questions?.length || 0} questions</span>
                </div>
            </div>
 
            <div className="qa-list">
                {data.questions?.map((question, index) => (
                    <div className="qa-card" key={question.id}>
                        <div className="qa-card-header">
                            <span className="q-number">Question {index + 1}</span>
                            <span className="q-difficulty">{question.difficulty}</span>
                        </div>
                        <div className="qa-card-body">
                            <div className="qa-field">
                                <label>Question</label>
                                <p>{question.question_text}</p>
                            </div>
 
                            {question.answer ? (
                                <>
                                    <div className="qa-field">
                                        <label>Your Answer</label>
                                        <p>{question.answer.answer_text}</p>
                                    </div>
                                    <div className="qa-field">
                                        <label>Score</label>
                                        <p className="score-inline">
                                            <span className={`score-badge ${getScoreClass(question.answer.score)}`} style={{ display: "inline-flex", width: "32px", height: "32px", fontSize: "0.85rem" }}>
                                                {question.answer.score}
                                            </span>
                                        </p>
                                    </div>
                                    <div className="qa-field">
                                        <label>Feedback</label>
                                        <p>{question.answer.feedback}</p>
                                    </div>
                                    <div className="qa-field">
                                        <label>Model Answer</label>
                                        <p>{question.answer.model_answer}</p>
                                    </div>
                                </>
                            ) : (
                                <p className="qa-not-answered">Not answered</p>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
 
export default SessionDetailPage