import { useState } from "react"
import { useNavigate } from "react-router-dom"


function RegisterPage(){
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")

    const navigate = useNavigate()

    const handleRegister = async () => {
        try{
            const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/register`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name: name, email: email, password: password})
            })

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
        }
    }

    return(
        <div>
            <h1>Register</h1>
            <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)}/>
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)}/>
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)}/>
            <button onClick={handleRegister}>Register</button>
            {error && <p>{error}</p>}
        </div>
    )
}

export default RegisterPage