import { useNavigate } from "react-router-dom";
import { FaPiggyBank } from "react-icons/fa6";
import { BsArrowLeft } from "react-icons/bs";
import { IoSettingsOutline } from "react-icons/io5";

import { logout } from "../api/auth.api";
import Button from "./Button";


const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    window.location.href = "/";
  };

  return (
    <nav className="navbar sticky-top navbar-expand-lg bg-secondary shadow-sm">
      <div className="container-fluid d-flex align-items-center py-2">
        <h2 className="navbar-brand mb-0" style={{ cursor: "pointer" }} onClick={() => navigate("/transactions")}>
          <FaPiggyBank className="me-2"/> 
          piggybank
        </h2>
        <Button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </Button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav navbar-nav-scroll d-flex align-items-center">
            <li className="nav-item">
              <p className="nav-link mb-0" style={{ cursor: "pointer" }} onClick={() => navigate("/transactions")}>transactions</p>
            </li>
            <li className="nav-item">
              <p className="nav-link mb-0" style={{ cursor: "pointer" }} onClick={() => navigate("/goals")}>goals</p>
            </li>
            <li className="nav-item">
              <p className="nav-link mb-0" style={{ cursor: "pointer" }} onClick={() => navigate("/categories")}>categories</p>
            </li>
          </ul>

          <div className="row g-2 ms-auto align-items-center">
            <div className="col-12 col-sm-auto">
              <Button variant="secondary" className="w-100" icon={IoSettingsOutline} onClick={() => navigate("/settings")}>settings</Button>
            </div>
            <div className="col-12 col-sm-auto">
              <Button variant="secondary" className="w-100" icon={BsArrowLeft} onClick={handleLogout}>logout</Button>
            </div>
          </div>

        </div>
      </div>
    </nav>
  );
};

export default Navbar;