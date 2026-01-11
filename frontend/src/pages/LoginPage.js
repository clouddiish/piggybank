
import React from "react";
import LoginForm from "../features/auth/LoginForm";
import { login } from "../api/auth.api";

const LoginPage = () => {
  const handleLogin = async (email, password) => {
    const response = await login(email, password);
    localStorage.setItem("token", response.data.access_token);
    window.location.reload();
  };

  return <LoginForm onLogin={handleLogin} />;
};

export default LoginPage;
