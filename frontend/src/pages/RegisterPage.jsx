import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { apiRequest } from "../api"


function RegisterPage(){
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    const handleRegister = async () => {
        if (!name.trim()) {
            setError("Please enter your name")
            return
        }
        if (!email.trim()) {
            setError("Please enter your email")
            return
        }
        if (password.length < 8) {
            setError("Password must be at least 8 characters")
            return
        }
        
        if (loading) return          
        setLoading(true)

        try{
            const response = await apiRequest("/auth/register", "POST", {name: name, email: email, password: password})

            const data = await response.json()

            if(response.ok){
                navigate("/")
            } else{
                if(typeof data.detail === "string"){
                    setError(data.detail)
                }
                else{
                    setError("All fields are mandatory")
                }
            }
        } catch(err){
            setError("Cannot connect to server")
        } finally {
            setLoading(false)
        }
    }

    return(
        <div>
            <h1>Register</h1>
            <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)}/>
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
            <button onClick={handleRegister} disabled={loading}>
                {loading ? "Registering..." : "Register"}
            </button>
            {error && <p>{error}</p>}
        </div>
    )
}

export default RegisterPage