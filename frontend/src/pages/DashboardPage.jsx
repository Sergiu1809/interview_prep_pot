import { useState } from "react"
import { useNavigate} from "react-router-dom"
import { apiRequest } from "../api"


function DashboardPage(){
    const [topic, setTopic] = useState("")
    const [error, setError] = useState("")

    const navigate = useNavigate()

    const createSession = async () => {

        if (!topic.trim()) {
            setError("Please enter a topic")
            return
        }

        try{
            const response = await apiRequest("/sessions/", "POST", {topic: topic})

            const data = await response.json()

            if(response.ok){
                navigate(`/interview/${data.id}`)
            } else {
                if ( typeof data.detail === "string") {
                    setError(data.detail)
                } else{
                    setError("Please enter a topic")
                }
            }
        } catch(err){
                setError("Cannot connect to server")
        }
    }

    return( 
    <div>
        <h1>Dashboard Page</h1>
        <input type="text" placeholder="Name session" value={topic} onChange={(e) => setTopic(e.target.value)}/>
        <button onClick={createSession}>Create Session</button>
        {error && <p>{error}</p>}
        <button onClick={() => navigate("/history")}>View History</button>
    </div>  
    
    )
}

export default DashboardPage