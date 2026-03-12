import { useNavigate } from "react-router-dom";
import { BsChevronLeft } from "react-icons/bs";

import { login } from "../api/auth.api";
import Button from "../components/Button";
import LoginForm from "../features/auth/LoginForm";


const LoginPage = () => {
  const navigate = useNavigate();
  const handleLogin = async (email, password) => {
    await login(email, password);
    window.location.reload();
  };

  return (
    <div className="mx-md-5 mx-2 py-5 align-items-center vh-100">
      <Button 
        variant="secondary" 
        icon={BsChevronLeft}
        onClick={() => navigate("/")}
        className="mb-5"
      />
      <h1 className="mb-5">welcome back! please log in</h1>
      <LoginForm onLogin={handleLogin} />
    </div>
  );
};

export default LoginPage;
