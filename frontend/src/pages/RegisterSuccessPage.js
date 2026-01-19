import { useNavigate } from "react-router-dom";

import Button from "../components/Button";


const RegisterSuccessPage = () => {
  const navigate = useNavigate();
  return (
    <>
      <h1>successfully registered</h1>
      <p>you can log in now</p>
      <Button variant="primary" onClick={() => navigate("/login")}>login</Button>
    </>
  );
}

export default RegisterSuccessPage;