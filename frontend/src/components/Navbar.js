import { useState } from "react";
import { HiOutlineBars3 } from "react-icons/hi2";

import Menu from "./Menu";


const Navbar = () => {
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <nav style={{ display: "flex", alignItems: "center", padding: "8px 16px", background: "#1976d2", color: "#fff" }}>
        <h2 style={{ flex: 1 }}>piggybank</h2>
        <button
            style={{ background: "none", border: "none", color: "#fff", fontSize: "24px", cursor: "pointer" }}
            onClick={() => setMenuOpen((open) => !open)}
        >
            <HiOutlineBars3 />
        </button>
        {menuOpen && <Menu onClose={() => setMenuOpen(false)} />}
        </nav>
    );
};

export default Navbar;