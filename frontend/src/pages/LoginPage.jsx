import { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginPage(){
    const[email,setEmail] = useState("")
    const[password, setPassword] = useState("")
    const[error,setError] = useState("")

    const navigate = useNavigate()

    const handleLogin = async () => {
        try{
            const response = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                headers: {"Content-Type": "application/x-www-form-urlencoded"},
                body: new URLSearchParams({username: email, password: password})
            })

            const data = await response.json()

            if(response.ok){
                localStorage.setItem("token", data.access_token)
                navigate("/dashboard")
            } else {
                setError(data.detail)
            }
        } catch(err){
            setError("Cannot connect to server")
        }
    }

    return(
        <div>
            <h1>Login</h1>
            <input
                type='email'
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>
            {error && <p>{error}</p>}
        </div>
    )
}

export default LoginPage