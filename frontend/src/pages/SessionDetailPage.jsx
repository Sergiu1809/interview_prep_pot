import {useState, useEffect} from  "react"
import { useParams } from "react-router-dom"
import { apiRequest } from "../api"

function SessionDetailPage(){
    const {sessionId} = useParams()
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState({})
    const [error, setError] = useState("")

    useEffect(() => {
        const fetchData = async () => {
            try{
                const response = await apiRequest(`/sessions/history/${sessionId}`, "GET")
                const data = await response.json()

                if(response.ok){
                    setData(data)
                }
            } catch{
                setError("Cannot connect to server")
            } finally{
                setLoading(false)
            }
        }

        fetchData()

    }, [])
    
    if (loading) return <p>Loading...</p>
    if (error) return <p>{error}</p>

    return(
        <div>
            <p>Topic: {data.topic}</p>
            <p>Status: {data.status}</p>
            {data.questions.map(question => (
                <div key={question.id}>
                    <p>Question: {question.question_text}</p>
                    <p>Difficulty: {question.difficulty}</p>
                    {question.answer ? (
                        <>
                            <p>Answer: {question.answer.answer_text}</p>
                            <p>Score: {question.answer.score}</p>
                            <p>Feedback: {question.answer.feedback}</p>
                            <p>Model Answer: {question.answer.model_answer}</p>
                        </>
                    ) : (
                         <p>Not answered</p>
                    )}
                </div>
            ))}
        </div>
    )
}

export default SessionDetailPage