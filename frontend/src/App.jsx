import { BrowserRouter, Routes, Route} from "react-router-dom"
import AuthGuard from "./components/ProtectedRoute"
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
        
        <Route element={<AuthGuard />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/interview/:sessionId" element={<InterviewPage />} />
          <Route path="/history" element={<HistoryPage/> } />
          <Route path="/history/:sessionId" element={<SessionDetailPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App