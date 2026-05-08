import { useNavigate } from "react-router-dom";
import { FaPiggyBank } from "react-icons/fa6";

import Button from "../components/Button";


const StartPage = () => {
  const navigate = useNavigate();
  return (
    <div className="mx-md-5 mx-2 py-5 align-items-center vh-100">

      <div className="my-5">
        <h1 className="display-1 fw-bold mb-3">
          <FaPiggyBank className="me-3"/>
          piggybank
        </h1>
        <h2>manage your personal finances</h2>
      </div>

      <div className="row g-3">
        <div className="col-12 col-md-auto">
          <Button variant="primary" className="w-100" onClick={() => navigate('/login')}>login</Button>
        </div>
        <div className="col-12 col-md-auto">
          <Button variant="secondary" className="w-100" onClick={() => navigate('/register')}>register</Button>
        </div>
      </div>
      
    </div>
  );
};

export default StartPage;