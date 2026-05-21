import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { apiRequest } from "../api"


function HistoryPage(){
    const [data, setData] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    useEffect(() => {
        const fetchData = async () => {
            try{
                const response = await apiRequest("/sessions/history/", "GET")
                const data = await response.json()

                if (response.ok){
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


    if (loading) return <p>Loading...</p>
    if (error) return <p>{error}</p>

    return (
        <div>
            {data.map(session => (
                <div key={session.id}>
                    <Link to={`/history/${session.id}`}>{session.topic}</Link>
                    <p >Status: {session.status}</p>
                    <p>Questions: {session.total_questions}</p>
                    <p>Average Score: {session.average_score}</p>
                </div>
            ))}
        </div>
    )
}

export default HistoryPage