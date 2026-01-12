import { useNavigate } from "react-router-dom";
import { BsChevronLeft } from "react-icons/bs";

import { login } from "../api/auth.api";
import Button from "../components/Button";
import LoginForm from "../features/auth/LoginForm";


const LoginPage = () => {
    const navigate = useNavigate();
    const handleLogin = async (email, password) => {
        const response = await login(email, password);
        localStorage.setItem("token", response.data.access_token);
        window.location.reload();
    };

    return (
        <>
            <Button 
                variant="secondary" 
                icon={BsChevronLeft}
                onClick={() => navigate("/")}
            />
            <h1>welcome back! please log in</h1>
            <LoginForm onLogin={handleLogin} />
        </>
    );
};

export default LoginPage;
