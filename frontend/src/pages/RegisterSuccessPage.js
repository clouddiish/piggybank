import { useNavigate } from "react-router-dom";

import Button from "../components/Button";


const RegisterSuccessPage = () => {
  const navigate = useNavigate();
  return (
    <div className="mx-md-5 mx-2 py-5 align-items-center vh-100">

      <div className="my-5">
        <h1>successfully registered</h1>
        <p>you can log in now</p>
      </div>

      <div className="row g-3">
        <div className="col-12 col-sm-auto">
          <Button variant="primary" className="w-100" onClick={() => navigate("/login")}>login</Button>
        </div>
      </div>

    </div>
  );
}

export default RegisterSuccessPage;