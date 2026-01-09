
import { Outlet } from "react-router-dom";
import { useContext, useState, useEffect } from "react";
import { Bell, Menu } from "lucide-react";
import Navbar from "./Navbar";
import { AuthContext } from "./AuthContext";
import '../styles/main.css';

export default function Layout({ handleLogout }) {
  const { user } = useContext(AuthContext);
  const [searchQuery, setSearchQuery] = useState("");
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const handleSearch = (e) => setSearchQuery(e.target.value);
  const openSidebar = () => setSidebarOpen(true);
  const closeSidebar = () => setSidebarOpen(false);

  // lock body scroll when drawer open
  useEffect(() => {
    document.body.style.overflow = isSidebarOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [isSidebarOpen]);

  return (
    <div className="app-container">
      {/* Sidebar (controlled by Layout) */}
      <Navbar handleLogout={handleLogout} isOpen={isSidebarOpen} onClose={closeSidebar} />

      {/* Overlay for mobile drawer */}
      {isSidebarOpen && <div className="drawer-overlay" onClick={closeSidebar} />}

      <div className="main-content">
        <header className="topbar">
          {/* Hamburger on small screens */}
          <button
            className="mobile-menu-btn"
            aria-label="Open menu"
            aria-expanded={isSidebarOpen}
            onClick={openSidebar}
          >
            <Menu size={20} />
          </button>

          <h5 className="topbar-title">AgriBoost</h5>

          <div className="topbar-right">
            <input
              type="text"
              placeholder="Search..."
              className="search"
              value={searchQuery}
              onChange={handleSearch}
            />
            <div className="notification-icon">
              <Bell size={20} />
            </div>

            {/* small user preview in topbar (optional) */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", marginLeft: 8 }}>
              <span style={{ fontSize: 12, color: "#374151" }}>{user?.full_name || "Guest User"}</span>
              <span style={{ fontSize: 11, color: "#8b949e" }}>{user?.email || ""}</span>
            </div>
          </div>
        </header>

        <main className="page-content">
          <Outlet context={{ searchQuery }} />
        </main>
      </div>
    </div>
  );
}
