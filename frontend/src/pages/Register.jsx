import { useState, useContext } from "react";
import "../register.css";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";
import LoaderOverlay from "../components/LoaderOverlay";

export default function Register() {
  const [full_name, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [password, setPassword] = useState("");
  const [confirm_password, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { setUser } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setIsError(false);

    // Client-side confirm password check
    if (password !== confirm_password) {
      setMessage("❌ Passwords do not match.");
      setIsError(true);
      return;
    }
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/users/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ full_name, email, address, password, confirm_password }),
      });

      const data = await response.json();

      if (response.status === 201) {
  setMessage(" User registered successfully! Please verify OTP.");
  setIsError(false);

  // Reset form
  setFullName("");
  setEmail("");
  setAddress("");
  setPassword("");
  setConfirmPassword("");

  // Save minimal user in context
  setUser(data.user || { full_name, email, address });

  // Redirect to OTP after short delay
  setTimeout(() => {
          setLoading(false); // hide loader
          navigate("/verify-otp", { state: { userId: data.user_id } });
        }, 500);

} else {
  // Handle field-specific errors
  if (data?.email) {
    setMessage(`Email error: ${data.email}`);
  } else if (data?.password) {
    setMessage(`Password error: ${data.password}`);
  } else if (data?.confirm_password) {
    setMessage(`Confirm Password error: ${data.confirm_password}`);
  } else if (data?.full_name) {
    setMessage(`Name error: ${data.full_name}`);
  } else if (data?.detail) {
    setMessage(`${data.detail}`);
  } else {
    setMessage("Registration failed. Please try again.");
  }
  
  setIsError(true);
  setLoading(false);
}
    } catch (error) {
      console.error("Error:", error);
      setMessage("⚠️ Something went wrong. Try again later.");
      setIsError(true);
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <LoaderOverlay loading={loading} message="Registering your account..." />

      <form className="register-form" onSubmit={handleSubmit}>
        <h2>Register to Agriboost</h2>

        <input
          type="text"
          placeholder="Full Name"
          value={full_name}
          onChange={(e) => setFullName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Address (optional)"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirm_password}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />

        <button type="submit">Register</button>

        {message && (
          <p className={isError ? "error-message" : "success-message"}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}
