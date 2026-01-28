import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import './App.css';
import client from "./api/client";
import CategoriesPage from "./pages/CategoriesPage";
import GoalsPage from "./pages/GoalsPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import RegisterSuccessPage from "./pages/RegisterSuccessPage";
import SettingsPage from "./pages/SettingsPage";
import StartPage from "./pages/StartPage";
import TransactionsPage from "./pages/TransactionsPage";


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    if (sessionStorage.getItem("refreshFailed")) {
      setIsAuthenticated(false);
      return;
    }
    client.get("/users/me")
      .then(() => setIsAuthenticated(true))
      .catch(() => setIsAuthenticated(false));
  }, []);

  if (isAuthenticated === null) {
    return <div>loading...</div>;
  }

  return (
    <Router>
      <Routes>
        {!isAuthenticated ? (
          <>
            <Route path="/" element={<StartPage />} />
            <Route path="/login" element={<LoginPage />} /> 
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/register-success" element={<RegisterSuccessPage />} />
            <Route path="/*" element={<Navigate to="/" replace />} />
          </>
        ) : (
          <>
            <Route path="/transactions" element={<TransactionsPage />} />
            <Route path="/categories" element={<CategoriesPage />} />
            <Route path="/goals" element={<GoalsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/*" element={<Navigate to="/transactions" replace />} />
          </>
        )}
      </Routes>
    </Router>
  );
}

export default App;
