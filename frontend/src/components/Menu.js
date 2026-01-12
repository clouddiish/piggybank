import { Link, useNavigate } from "react-router-dom";
import { BsArrowLeft } from "react-icons/bs";
import { IoSettingsOutline } from "react-icons/io5";

import { logout } from "../api/auth.api";
import Button from "./Button";


const Menu = ({ onClose }) => {
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        window.location.reload();
    };

    return <div style={{
        position: "absolute",
        top: "56px",
        right: "16px",
        background: "#fff",
        color: "#333",
        border: "1px solid #ccc",
        borderRadius: "4px",
        padding: "16px",
        zIndex: 1000
    }}>
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            <li><Link to="/transactions" onClick={onClose}>transactions</Link></li>
            <li><Link to="/goals" onClick={onClose}>goals</Link></li>
            <li><Link to="/categories" onClick={onClose}>categories</Link></li>
        </ul>
        <Button variant="secondary" icon={IoSettingsOutline} onClick={() => navigate("/settings")}>settings</Button>
        <Button variant="secondary" icon={BsArrowLeft} onClick={handleLogout}>logout</Button>
    </div>
};

export default Menu;