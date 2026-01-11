import './App.css';

import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import HomeTest from "./pages/HomeTest";

function App() {
  const token = localStorage.getItem("token");

  return (
    <Router>
      <Routes>
        {!token ? (
          <>
            <Route path="/*" element={<LoginPage />} />
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
