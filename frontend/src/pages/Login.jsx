import React, { useState, useContext } from "react";
import "../LoginPage.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";
import LoaderOverlay from "../components/LoaderOverlay";


export default function Login({ setIsLoggedIn }) {
  const { loginUser } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  const navigate = useNavigate();

  const handleSubmit = async (e) => {
  e.preventDefault();
  setError("");
  setLoading(true);
  try {
    const res = await axios.post("http://127.0.0.1:8000/api/users/login/", {
      email,
      password,
    });

    // Save tokens
    localStorage.setItem("access", res.data.access);
    localStorage.setItem("refresh", res.data.refresh);

    // Save user object directly
    localStorage.setItem("user", JSON.stringify(res.data.user));

    // Update AuthContext so UI reflects current user immediately
    loginUser(res.data.user, { access: res.data.access, refresh: res.data.refresh });

    setIsLoggedIn(true);
     // hide loader
    navigate("/dashboard");
        
  } catch (err) {
    if (err.response) {
      setError(err.response.data.detail||"Invalid email or password!");
    } else {
      setError("Server unreachable. Please try again later.");
    }
  } finally {
  
  setLoading(false);
}
};

  return (
    <div className="login-container">
       <LoaderOverlay loading={loading} message="Logging in..." />
      <form className="login-form" onSubmit={handleSubmit}>
        <h2 className="login-title">Welcome Back 👋</h2>
        <p className="login-subtitle">Login to continue to Agriboost</p>

        {error && <p className="error-message">{error}</p>}

        <div className="input-group">
          <label htmlFor="email">Email Address</label>
          <input
            type="email"
            id="email"
            placeholder="example@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="login-options">
          <label className="remember-me">
            <input
              type="checkbox"
              checked={remember}
              onChange={(e) => setRemember(e.target.checked)}
            />
            Remember me
          </label>
          <a href="/forgot-password" className="forgot-link">
            Forgot password?
          </a>
        </div>

        <button type="submit" className="login-btn">
          Login
        </button>

        <p className="signup-text">
          Don’t have an account?{" "}
          <a href="/register" className="signup-link">
            Sign up
          </a>
        </p>
      </form>
    </div>
  );
}
