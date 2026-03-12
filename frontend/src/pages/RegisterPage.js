import { useNavigate } from "react-router-dom";
import { BsChevronLeft } from "react-icons/bs";

import { register } from "../api/auth.api";
import Button from "../components/Button";
import RegisterFrom from "../features/auth/RegisterForm";


const RegisterPage = () => {
  const navigate = useNavigate();
  const handleRegister = async (email, password, confirmPassword) => {
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    await register(email, password);
    navigate("/register-success");
  };

  return (
    <div className="mx-md-5 mx-2 py-5 align-items-center vh-100">
      <Button 
        variant="secondary" 
        icon={BsChevronLeft}
        onClick={() => navigate("/")}
        className="mb-5"
      />
      <h1 className="mb-5">hello! register to get started</h1>
      <RegisterFrom onRegister={handleRegister} />
    </div>
  );
};

export default RegisterPage;
