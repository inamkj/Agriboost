
import { NavLink } from "react-router-dom";
import logo from "../assets/images/logo.png";
import '../styles/main.css';
import {
  LayoutDashboard,
  Activity,
  History,
  Settings,
  LogOut,
  Leaf,
  User,
  X
} from "lucide-react";


export default function Navbar({ handleLogout, isOpen = false, onClose = () => {} }) {
  const navItems = [
    { id: "dashboard", label: "Dashboard", icon: <LayoutDashboard size={18} />, path: "/dashboard" },
    { id: "disease", label: "Disease Detection", icon: <Leaf size={18} />, path: "/disease" },
    { id: "iot", label: "Sensors Readings", icon: <Activity size={18} />, path: "/iot" },
    { id: "crophistory", label: "History", icon: <History size={18} />, path: "/crop-history" },
    { id: "history", label: "Profile History", icon: <User size={18} />, path: "/history" },
    { id: "settings", label: "Profile", icon: <Settings size={18} />, path: "/settings" },
  
  ];

  return (
    <aside className={`sidebar ${isOpen ? "open" : ""}`} aria-hidden={!isOpen && window.innerWidth < 769}>
      <div className="sidebar-top" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div className="logo">
          <img src={logo} alt="AgriBoost" className="logo-img" />
        </div>

        {/* close button: only visible on small screens */}
        <button className="close-btn" aria-label="Close menu" onClick={onClose}>
          <X size={18} />
        </button>
      </div>

      <nav className="nav">
        {navItems.map((item) => (
          <NavLink
            key={item.id}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
            onClick={onClose} /* close drawer after navigation on mobile */
          >
            {item.icon}
            <span className="label">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="logout">
        <button onClick={() => { onClose(); handleLogout && handleLogout(); }} className="nav-item logout-btn">
          <LogOut size={18} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}

