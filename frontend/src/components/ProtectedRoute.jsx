import {Outlet, Navigate, useNavigate } from "react-router-dom";

function AuthGuard(){
    const navigate = useNavigate()
    const token = localStorage.getItem("token")
    return token ? 
        <div>
            <button onClick={() => {
                localStorage.removeItem("token")
                 navigate("/")                   
            }}>Logout</button>
            <Outlet/>
        </div> : 
        <Navigate to="/"/>
}

export default AuthGuard