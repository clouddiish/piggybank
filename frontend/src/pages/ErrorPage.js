import { useNavigate } from "react-router-dom";

import Button from "../components/Button";


const ErrorPage = () => {
  const navigate = useNavigate();
  return (
    <div className="mx-md-5 mx-2 py-5 align-items-center vh-100">
      <div className="my-5">
        <h1 className="fw-bold mb-3">something went wrong :-(</h1>
        <p className="mb-5">please contact support if the problem persists</p>
      </div>
      <div className="row g-3">
        <div className="col-12 col-md-auto">
          <Button variant="primary" className="w-100" onClick={() => navigate('/')}>go to home page</Button>
        </div>
      </div>
    </div>
  );
};

export default ErrorPage;