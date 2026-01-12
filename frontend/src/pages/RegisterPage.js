import { useNavigate } from "react-router-dom";
import { BsChevronLeft } from "react-icons/bs";

import { register } from "../api/auth.api";
import Button from "../components/Button";
import RegisterFrom from "../features/auth/RegisterForm";


const RegisterPage = () => {
    const navigate = useNavigate();
    const handleRegister = async (email, password) => {
        const response = await register(email, password);
        navigate("/register-success");
    };

    return (
        <>
            <Button 
                variant="secondary" 
                icon={BsChevronLeft}
                onClick={() => navigate("/")}
            />
            <h1>hello! register to get started</h1>
            <RegisterFrom onRegister={handleRegister} />
        </>
    );
};

export default RegisterPage;
