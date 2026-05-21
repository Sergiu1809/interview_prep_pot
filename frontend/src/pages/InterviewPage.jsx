import { useParams, useNavigate } from "react-router-dom"
import { apiRequest } from "../api"
import { useState } from "react"

function InterviewPage(){
    const {sessionId} = useParams()
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

    const generateQuestion = async () => {
        if (loading) return          
        setLoading(true) 
        setAnswer("")

        try{
            const response = await apiRequest(`/sessions/${sessionId}/next-question`,"POST", {difficulty: difficulty})

            const data = await response.json()

            if(response.ok){
                setQuestion(data.question_text)
                setQuestionId(data.id)
                setPhase("answering")
            }
        } catch { 
            setError("Cannot connect to server")
        } finally{
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
        
        
        try{
            const response = await apiRequest(`/sessions/${sessionId}/${questionId}/answer`, "POST", {answer_text: answer})

            const data = await response.json()

            if(response.ok){
                setPhase("feedback")
                setFeedback(data.feedback)
                setScore(data.score)
                setModelAnswer(data.model_answer)
            }
        } catch {
            setError("Cannot connect to server")
        } finally{
            setLoading(false)
        }
    }

    const completeSession = async () => {
        if (loading) return
        setLoading(true)

        try{
            const response = await apiRequest(`/sessions/${sessionId}/complete`,"PATCH")

            const data = await response.json()

            if(response.ok){
                navigate(`/history/${sessionId}`)
            }
        } catch {
            setError("Cannot connect to server")
        } finally{
            setLoading(false)
        }
    }


    return(
        <div>         
            {phase === "choosing" && (
                <div>
                    <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                        <option value="easy">Easy</option>
                        <option value ="medium">Medium</option>
                        <option value="hard">Hard</option>
                    </select>
                    <button onClick={generateQuestion} disabled={loading}>{loading ? "Generating..." : "Generate Question"}</button>
                    {error && <p>{error}</p>}
                </div>
                )}
            
            {phase === "answering" && (
                <div>
                    <p>{question}</p>
                    <textarea value={answer} placeholder="Your answer..."  onChange={(e) => setAnswer(e.target.value)}></textarea>
                    <button onClick={submitAnswer} disabled={loading} >{loading ? "Submitting..." : "Submit"}</button>
                    {error && <p>{error}</p>} 
                </div>
            )}

            {phase === "feedback" && (
                <div>
                    {score && <p>{score}</p>}
                    {feedback && <p>{feedback}</p>}
                    {modelAnswer && <p>{modelAnswer}</p>}
                    <button onClick={() => setPhase("choosing")}>Next Question</button>
                    <button onClick={completeSession} disabled={loading}>
                        {loading ? "Completing..." : "Complete Session"}
                    </button>
                </div>
            )}
        </div>
    )
}

export default InterviewPage