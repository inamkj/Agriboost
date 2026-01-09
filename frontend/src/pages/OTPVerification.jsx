import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "../styles/OtpVerification.css";

export default function OTPVerification() {
  const [otp, setOtp] = useState("");
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();

  // we passed user_id in navigate state
  const { userId } = location.state || {};

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userId) {
      setMessage("❌ Missing user ID. Please register again.");
      setIsError(true);
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/api/users/verify-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, otp }),
      });

      const data = await res.json();

      if (res.status === 200) {
        setMessage("✅ OTP verified successfully! Redirecting...");
        setIsError(false);

        // Save tokens
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));

        // Redirect to dashboard after 1s
        setTimeout(() => navigate("/login"), 1000);
      } else {
        setMessage(data.detail || "❌ Invalid OTP. Please try again.");
        setIsError(true);
      }
    } catch (err) {
      console.error("Error:", err);
      setMessage("⚠️ Server error. Try again later.");
      setIsError(true);
    }
  };

  return (
    <div className="otp-container">
      <form className="otp-form" onSubmit={handleSubmit}>
        <h2>Verify Your Email</h2>
        <p>Please enter the OTP sent to your email.</p>

        <input
          type="text"
          placeholder="Enter OTP"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
          required
        />

        <button type="submit">Verify OTP</button>

        {message && (
          <p className={isError ? "error-message" : "success-message"}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
}
