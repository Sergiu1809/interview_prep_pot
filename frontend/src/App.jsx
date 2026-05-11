  // function App(){
  //   const name = 'Sergiu'
  //   const project = 'PrepAI'
  //   return(
  //     <div className="container">
  //       <h1>Hello, {name}!</h1>
  //       <h1>Welcome to {project}</h1>
  //     </div>
  //   )
  // }

  // export default App;

 // -----------------------------------------------------  

// import { useState } from "react";

// function App(){
//   const [count, setCount] = useState(0)
//     //     ^value  ^setter    ^initial value

//   return(
//     <div>
//      <p>Count: {count}</p>
//      <button onClick={() => setCount(count+1)}>Add 1</button>
//     </div>
//   )
// }

// export default App;

// -------------------------------------------------------

// import { useState } from "react";

// function App(){
//   const [isVisible, setIsVisible] = useState(false)
//   return (
//     <div>
//     <button onClick={() => setIsVisible(!isVisible)}>
//       {isVisible ? 'Hide message' : "Show message"}
//     </button>

//     { isVisible && <p>Hello, I am now visible</p>}
//     </div>
//   )
// }

// export default App;

// ------------------------------------------------------

// import { useState } from 'react'

// function App(){
//   const [email, setEmail] = useState("")
//   const [password, setPassword] = useState("")
//   const [message, setMessage] = useState("")
//   return(
//     <div>
//       <p>Email:</p>
//       <input type='email' value={email} onChange={(e) => setEmail(e.target.value)}/>
//       <p>Password:</p>
//       <input type='password' value={password} onChange={(e) => setPassword(e.target.value)}/>
//       <button onClick={() => setMessage("Email is not formatted well") }>Click</button>
//       <p>{message}</p>
//     </div>
//   )
// }

// export default App;


// import { useState } from "react";

// function App(){
//   const [email, setEmail] = useState("")
//   const [password, setPassword] = useState("")
//   const [message, setMessage] = useState("")
//   return (
//     <div className="container">
//       <p>Email:</p>
//       <input type='email' value = {email} onChange={(e) => setEmail(e.target.value)}/>
//       <p>Password:</p>
//       <input type='password' value={password} onChange={(e) => setPassword(e.target.value)}/>
//       <button onClick={() => setMessage(email)}>Submit</button>
//       <p>{message}</p>
//     </div>
//   )
// }

// export default App

// import { useState } from "react";

// function App(){
//   const [username, setUsername] = useState("")
//   const [email, setEmail] = useState("")
//   const [password, setPassword] = useState("")
//   const [showSummary, setShowSummary] = useState(false)
//   return(
//     <div className="container">
//       <p>Username:</p>
//       <input type='text' value={username} onChange={(e) => setUsername(e.target.value)}/>
//       <p>Email:</p>
//       <input type='email' value={email} onChange={(e) => setEmail(e.target.value)}/>
//       <p>Password:</p>
//       <input type='password' value={password} onChange={(e) => setPassword(e.target.value)}></input>
//       <button onClick={() => setShowSummary(username && email && password)
//       }>Submit</button>

//     {showSummary &&  <div className="summary">
//         <p>Username: {username}</p>
//         <p>Email: {email}</p>
//         <p>Password: {password ? "********" : ""}</p>
//       </div> }

//     {!showSummary && <p>Please fill in all fields</p>}
//     </div> 
//   )
// }

// export default App

// import { useState } from "react";

// function App(){
//   const [username, setUsername] = useState("")
//   const [email, setEmail] = useState("")
//   const [password, setPassword] = useState("")
//   const [showSummary, setShowSummary] = useState(false)
//   return (
//     <div className="container">
//       <p>Username:</p>
//       <input type='text' value={username} onChange={(e) => setUsername(e.target.value)}/>
//       <p>Email:</p>
//       <input type='email' type={email} onChange={(e) => setEmail(e.target.value)}/>
//       <p>Password:</p>
//       <input type='password' type={password} onChange={(e) => setPassword(e.target.value)}/>
//       <button onClick={() => setShowSummary(username && email && password)}>Submit</button>

//       {showSummary && <div className="summary">
//          <p>Username: {username}</p>
//          <p>Email: {email}</p>
//         <p>Password: {password ? "********" : ""}</p>
//       </div>}

//       {!showSummary && "Please fill in all fields"}
//     </div>
//   )

// }

// export default App

// import {useState, useEffect} from "react"

// function App(){
//   const [sessions, setSessions] = useState([])

//   useEffect(() => {
//     console.log("Component loaded!")
//       // this is where you'll call your FastAPI backend
//   }, []) // the dependency array

//   return (
//      <div>Hello</div>
//   )
// }

// import { useState, useEffect } from "react";

// function App(){
//   const [message, setMessage] = useState("")
  
//   useEffect(() => {
//     setMessage("Data loaded!")
//   },[])

//   return(
//     <p>{message}</p>
//   )
// }

// export default App

import { BrowserRouter, Routes, Route} from "react-router-dom"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"
import InterviewPage from "./pages/InterviewPage"
import DashboardPage from "./pages/DashboardPage"
import SessionDetailPage from "./pages/SessionDetailPage"
import HistoryPage from "./pages/HistoryPage"

function App(){
  return(
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/interview/:sessionId" element={<InterviewPage />} />
        <Route path="/history" element={<HistoryPage/> } />
        <Route path="/history/:sessionId" element={<SessionDetailPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App