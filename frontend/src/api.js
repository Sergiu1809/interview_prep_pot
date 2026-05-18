export async function apiRequest(path, method = "GET", body = null){
        const headers = {"Content-Type": "application/json"}

        const token = localStorage.getItem("token")

        if(token){
            headers["Authorization"] = `Bearer ${token}`
        }

        const response = await fetch(`${import.meta.env.VITE_API_URL}${path}`,{
            method: method,
            headers: headers,
            body: body ? JSON.stringify(body) : null
        }) 

        return response
}