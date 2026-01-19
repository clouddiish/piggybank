import { useNavigate } from "react-router-dom";

import Button from "../components/Button";


const StartPage = () => {
  const navigate = useNavigate();
  return (
    <>
      <h1>piggybank</h1>
      <h2>manage your personal finances</h2>
      <Button variant="primary" onClick={() => navigate("/login")}>login</Button>
      <Button variant="secondary" onClick={() => navigate("/register")}>register</Button>
    </>
  );
};

export default StartPage;