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

    const navigate = useNavigate()

    const generateQuestion = async () => {
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
        }
    }

    const submitAnswer = async () => {
        if (!answer.trim()) {
            setError("Please enter an answer")
            return
        }
        setError("")
        
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
        }
    }

    const completeSession = async () => {
        try{
            const response = await apiRequest(`/sessions/${sessionId}/complete`,"PATCH")

            const data = await response.json()

            if(response.ok){
                navigate(`/history/${sessionId}`)
            }
        } catch {
            setError("Cannot connect to server")
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
                    <button onClick={generateQuestion}>Generate Question</button>
                    {error && <p>{error}</p>}
                </div>
                )}
            
            {phase === "answering" && (
                <div>
                    <p>{question}</p>
                    <textarea value={answer} placeholder="Your answer..."  onChange={(e) => setAnswer(e.target.value)}></textarea>
                    <button onClick={submitAnswer}>Submit</button>
                    {error && <p>{error}</p>} 
                </div>
            )}

            {phase === "feedback" && (
                <div>
                    {score && <p>{score}</p>}
                    {feedback && <p>{feedback}</p>}
                    {modelAnswer && <p>{modelAnswer}</p>}
                    <button onClick={() => setPhase("choosing")}>Next Question</button>
                    <button onClick={completeSession}>Complete Session</button>
                </div>
            )}
        </div>
    )
}

export default InterviewPage