import "../styles/dashboard.css";
import { Link } from "react-router-dom";
import CropHealthCharts from "../components/CropHealthCharts";
export default function Dashboard() {
  return (
    <>
      {/* Hero Banner */}
      <div className="hero-banner" role="region" aria-label="Welcome banner">
        <div className="hero-content" >
          
          <p>
            AI-powered disease detection & real-time IoT monitoring for healthier fields.
          </p>
          <Link to="/about" className="btn hero-btn">Learn More</Link>
        </div>
      </div>

      {/* Dashboard Features */}
      <div className="dashboard-grid">
        <div className="card">
          <h3>Disease Detection</h3>
          <p>Run our AI model on crop images instantly.</p>
          <Link to="/disease" className="btn">Detect </Link>
        </div>

        <div className="card">
          <h3>Sensors Readings</h3>
          <p>Monitor soil conditions live by using sensors.</p>
          <Link to="/iot" className="btn">Readings</Link>
        </div>

        <div className="card">
          <h3>History</h3>
          <p>Access your past detections and insights.</p>
          <Link to="/crop-history" className="btn">History</Link>
        </div>
      </div>
      <CropHealthCharts />

      {/* Info Section */}
      <div className="info-card">
        <h2>About Sugarcane</h2>
        <p>
          Sugarcane is one of the world’s most important crops, widely grown in
          tropical & subtropical regions. It’s cultivated for sugar, ethanol,
          paper production—and supports millions of farmers globally.
        </p>
      </div>
    </>
  );
}
