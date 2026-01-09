import { useNavigate } from "react-router-dom";
import "../styles/Home.css";
import logo from "../assets/images/logo.png";
import { useState } from "react";
import LoaderOverlay from "../components/LoaderOverlay";

export default function Home() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleNav = (path) => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigate(path);
    }, 500); // small delay so spinner is visible
  };

   return (
    <div className="home-container">
      <LoaderOverlay loading={loading} message="Please wait..." />

      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">
          <img src={logo} alt="AgriBoost" style={{ width: "80px", height: "auto" }} />
        </div>
        <div className="nav-links">
          <button className="nav-btn" onClick={() => handleNav("/login")}>
            Login
          </button>
          <button className="nav-btn signup" onClick={() => handleNav("/register")}>
            Sign Up
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Boost Your Farming with AI & IoT</h1>
          <p>
            Agriboost helps farmers detect plant diseases, monitor soil health,
            and get smart fertilizer recommendations.
          </p>
          <div className="cta-buttons">
            <button className="cta-btn" onClick={() => handleNav("/login")}>
              Login
            </button>
            <button className="cta-btn outline" onClick={() => handleNav("/register")}>
              Sign Up
            </button>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="services">
        <h2>Our Services</h2>
        <div className="service-cards">
          <div className="card">
            <h3>🌿 Disease Detection</h3>
            <p>Upload crop images and get instant AI-powered disease diagnosis.</p>
          </div>
          <div className="card">
            <h3>🌍 IoT Soil Monitoring</h3>
            <p>Real-time soil data (pH, moisture, temperature) for smarter decisions.</p>
          </div>
          <div className="card">
            <h3>💡 Fertilizer Suggestions</h3>
            <p>Get personalized fertilizer plans to improve crop yield sustainably.</p>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <footer className="footer">
        <p>Ready to boost your farming?</p>
        <div className="cta-buttons">
          <button className="cta-btn" onClick={() => handleNav("/login")}>
            Login
          </button>
          <button className="cta-btn outline" onClick={() => handleNav("/register")}>
            Sign Up
          </button>
        </div>
      </footer>
    </div>
  );
}
