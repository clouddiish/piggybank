import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import './App.css';
import CategoriesPage from "./pages/CategoriesPage";
import GoalsPage from "./pages/GoalsPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import RegisterSuccessPage from "./pages/RegisterSuccessPage";
import SettingsPage from "./pages/SettingsPage";
import StartPage from "./pages/StartPage";
import TransactionsPage from "./pages/TransactionsPage";


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
