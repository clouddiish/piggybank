import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import './App.css';
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import RegisterSuccessPage from "./pages/RegisterSuccessPage";
import StartPage from "./pages/StartPage";
import HomeTest from "./pages/HomeTest";


function App() {
  const token = localStorage.getItem("token");

  return (
    <Router>
      <Routes>
        {!token ? (
          <>
            <Route path="/" element={<StartPage />} />
            <Route path="/login" element={<LoginPage />} /> 
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/register-success" element={<RegisterSuccessPage />} />
            <Route path="/*" element={<Navigate to="/" replace />} />
          </>
        ) : (
          <>
            <Route path="/" element={<HomeTest />} />
            <Route path="/*" element={<Navigate to="/" replace />} />
          </>
        )}
      </Routes>
    </Router>
  );
}

export default App;
