import "../styles/main.css";
import logo from "../assets/images/logo.png";
import image2 from "../assets/images/murtaza.jpg";
import image3 from "../assets/images/inam.jpg";
import image4 from "../assets/images/image2.png";
import image5 from "../assets/images/image4.jpg";

export default function About() {
  return (
    <div className="about-page">
      {/* Hero */}
      <section
        className="about-hero"
        role="region"
        aria-label="About AgriBoost"
        style={{
          backgroundImage: `linear-gradient(120deg, rgba(145,185,79,0.7), rgba(183,219,121,0.6)), url(${image5})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <div className="about-hero__content">
          <h1>About AgriBoost</h1>
          <p>
            Empowering modern agriculture with AI-driven disease detection and real-time IoT insights.
          </p>
        </div>
      </section>

      {/* Split: About text + image */}
      <section className="about-split">
        <div className="about-split__text card">
          <h2>What We Do</h2>
          <p>
            AgriBoost helps farmers and researchers monitor crop health by combining computer vision
            disease detection with on-field sensor data. Our platform centralizes predictions,
            soil metrics (pH, moisture, temperature), and activity history to support smarter,
            faster decisions.
          </p>
          <ul className="about-list">
            <li>AI disease detection from leaf images</li>
            <li>IoT soil monitoring and trend analysis</li>
            <li>Secure user accounts and activity history</li>
            <li>Clean, responsive UI for all devices</li>
          </ul>
        </div>
        <div className="about-split__media card">
          <img src={image4} alt="AgriBoost" className="about-image" />
        </div>
      </section>

      {/* Team */}
      <section className="team-section">
        <h2 className="section-title" style={{ marginBottom: 12 }}>Developers</h2>
        <div className="team-grid">
          <div className="team-card">
            <img src={image3} alt="Inamullah" className="team-cover" />
            <div className="team-info">
              <h3>Inamullah</h3>
              <p>Full‑stack developer focusing on Django REST APIs, data models, and
                integration of AI disease detection with secure authentication.</p>
            </div>
          </div>
          <div className="team-card">
            <img src={image2} alt="Ghulam Murtza" className="team-cover" />
            <div className="team-info">
              <h3>Ghulam Murtza</h3>
              <p>Frontend engineer specializing in React UI/UX, responsive design,
                and seamless data visualizations for sensor analytics.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
