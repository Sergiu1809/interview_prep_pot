import { useParams, useNavigate } from "react-router-dom"
import { apiRequest } from "../api"
import { useState } from "react"
 
function InterviewPage() {
    const { sessionId } = useParams()
    const [phase, setPhase] = useState("choosing")
    const [difficulty, setDifficulty] = useState("easy")
    const [question, setQuestion] = useState("")
    const [questionId, setQuestionId] = useState("")
    const [answer, setAnswer] = useState("")
    const [feedback, setFeedback] = useState("")
    const [score, setScore] = useState("")
    const [modelAnswer, setModelAnswer] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
 
    const navigate = useNavigate()
 
    const getScoreClass = (score) => {
        if (score >= 7) return "high"
        if (score >= 4) return "mid"
        return "low"
    }
 
    const generateQuestion = async () => {
        if (loading) return
        setLoading(true)
        setAnswer("")
        setError("")
 
        try {
            const response = await apiRequest(
                `/sessions/${sessionId}/next-question`, "POST",
                { difficulty: difficulty }
            )
 
            const data = await response.json()
 
            if (response.ok) {
                setQuestion(data.question_text)
                setQuestionId(data.id)
                setPhase("answering")
            }
        } catch {
            setError("Cannot connect to server")
        } finally {
            setLoading(false)
        }
    }
 
    const submitAnswer = async () => {
        if (!answer.trim()) {
            setError("Please enter an answer")
            return
        }
        setError("")
        if (loading) return
        setLoading(true)
 
        try {
            const response = await apiRequest(
                `/sessions/${sessionId}/${questionId}/answer`, "POST",
                { answer_text: answer }
            )
 
            const data = await response.json()
 
            if (response.ok) {
                setPhase("feedback")
                setFeedback(data.feedback)
                setScore(data.score)
                setModelAnswer(data.model_answer)
            }
        } catch {
            setError("Cannot connect to server")
        } finally {
            setLoading(false)
        }
    }
 
    const completeSession = async () => {
        if (loading) return
        setLoading(true)
 
        try {
            const response = await apiRequest(
                `/sessions/${sessionId}/complete`, "PATCH"
            )
 
            const data = await response.json()
 
            if (response.ok) {
                navigate(`/history/${sessionId}`)
            }
        } catch {
            setError("Cannot connect to server")
        } finally {
            setLoading(false)
        }
    }
 
    return (
        <div>
            <div className="interview-header">
                <h1>Interview Session</h1>
                <p>Session #{sessionId}</p>
            </div>
 
            {phase === "choosing" && (
                <div className="interview-phase">
                    <p className="question-label">Select difficulty</p>
                    <div className="choosing-row">
                        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                            <option value="easy">Easy</option>
                            <option value="medium">Medium</option>
                            <option value="hard">Hard</option>
                        </select>
                        <button
                            className="btn btn-primary"
                            onClick={generateQuestion}
                            disabled={loading}
                        >
                            {loading ? "Generating..." : "Generate Question"}
                        </button>
                    </div>
                    {error && <p className="error-msg">{error}</p>}
                </div>
            )}
 
            {phase === "answering" && (
                <div className="interview-phase">
                    <p className="question-label">Question</p>
                    <p className="question-text">{question}</p>
                    <div className="answer-section">
                        <textarea
                            value={answer}
                            placeholder="Type your answer here..."
                            onChange={(e) => setAnswer(e.target.value)}
                        />
                        <button
                            className="btn btn-accent"
                            onClick={submitAnswer}
                            disabled={loading}
                        >
                            {loading ? "Evaluating..." : "Submit Answer"}
                        </button>
                    </div>
                    {error && <p className="error-msg">{error}</p>}
                </div>
            )}
 
            {phase === "feedback" && (
                <div className="interview-phase">
                    <div className="feedback-card">
                        <div className="feedback-score">
                            <span className={`score-badge ${getScoreClass(score)}`}>
                                {score}
                            </span>
                            <span>out of 10</span>
                        </div>
 
                        <div className="feedback-section feedback-text">
                            <p className="section-label">Feedback</p>
                            <p>{feedback}</p>
                        </div>
 
                        <div className="feedback-section model-answer">
                            <p className="section-label">Model Answer</p>
                            <p>{modelAnswer}</p>
                        </div>
 
                        <div className="btn-group">
                            <button
                                className="btn btn-primary"
                                onClick={() => setPhase("choosing")}
                            >
                                Next Question
                            </button>
                            <button
                                className="btn btn-secondary"
                                onClick={completeSession}
                                disabled={loading}
                            >
                                {loading ? "Completing..." : "Complete Session"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
 
export default InterviewPage