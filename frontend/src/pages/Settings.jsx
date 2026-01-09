import "../styles/main.css";
import { useEffect, useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../components/AuthContext";

export default function Settings() {
  const { user, setUser } = useContext(AuthContext);
  const [formData, setFormData] = useState({ full_name: "", email: "" });
  const [passwordData, setPasswordData] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [profileError, setProfileError] = useState("");
  const [profileSuccess, setProfileSuccess] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState("");

  // Prefill form when user context changes
  useEffect(() => {
    if (user) setFormData({ full_name: user.full_name, email: user.email });
  }, [user]);

  const token = localStorage.getItem("access");

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    if (!token) return alert("You are not logged in!");

    try {
      setProfileError("");
      setProfileSuccess("");
      const res = await axios.put(
        "http://127.0.0.1:8000/api/users/profile/",
        formData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setUser(res.data);
      localStorage.setItem("user", JSON.stringify(res.data));
      setProfileSuccess("Profile updated successfully!");
    } catch (err) {
      const data = err.response?.data;
      if (data) {
        const msg = data.email || data.full_name || data.detail || "Profile update failed";
        setProfileError(typeof msg === "string" ? msg : JSON.stringify(msg));
      } else {
        setProfileError("Server error. Try again later.");
      }
    }
  };

  // const handleChangePassword = async (e) => {
  //   e.preventDefault();
  //   if (!token) return alert("You are not logged in!");

  //   try {
  //     await axios.put(
  //       "http://127.0.0.1:8000/api/users/change-password/",
  //       passwordData,
  //       { headers: { Authorization: `Bearer ${token}` } }
  //     );
  //     alert("Password changed successfully!");
  //     setPasswordData({ old_password: "", new_password: "", confirm_password: "" });
  //   } catch (err) {
  //     console.error(
  //       "Password change error:",
  //       err.response?.data || err.message
  //     );
  //   }
  // };
const handleChangePassword = async (e) => {
  e.preventDefault();
  if (!token) return alert("You are not logged in!");
  
  if (passwordData.new_password !== passwordData.confirm_password) {
    setPasswordError("New password and confirmation do not match!");
    setPasswordSuccess("");
    return;
  }

  try {
    setPasswordError("");
    setPasswordSuccess("");
    const res = await axios.put(
      "http://127.0.0.1:8000/api/users/change-password/",
      {
        old_password: passwordData.old_password,
        new_password: passwordData.new_password,
      },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    setPasswordSuccess(res.data?.message || "Password changed successfully!");
    setPasswordData({ old_password: "", new_password: "", confirm_password: "" });
  } catch (err)  {
    const data = err.response?.data;
    if (data) {
      // Show old password error
      if (data.old_password) setPasswordError(data.old_password);
      // Show new password error
      if (data.new_password) setPasswordError(data.new_password[0]);
      // Other errors
      if (!data.old_password && !data.new_password) setPasswordError("Password change failed!");
    } else {
      setPasswordError("Server error. Try again later.");
    }
  }
};
  return (
    <div className="settings-container">
      {/* <h2 className="settings-title">User Settings</h2> */}

      <div className="settings-card">
        {/* --- Profile Section --- */}
        <div className="section">
          <h3 className="section-title">Profile Information</h3>
          <form onSubmit={handleUpdateProfile} className="form-grid">
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) =>
                  setFormData({ ...formData, full_name: e.target.value })
                }
                placeholder="Full Name"
                required
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                placeholder="Email Address"
                required
              />
            </div>

            <button type="submit" className="btn btn-primary">
              Save Changes
            </button>
            {profileSuccess && <div className="success-message">{profileSuccess}</div>}
            {profileError && <div className="error-message">{profileError}</div>}
          </form>
        </div>

        {/* --- Password Section --- */}
        <div className="section">
          <h3 className="section-title">Change Password</h3>
          <form onSubmit={handleChangePassword} className="form-grid">
            <div className="form-group">
              <label>Old Password</label>
              <input
                type="password"
                value={passwordData.old_password}
                onChange={(e) =>
                  setPasswordData({ ...passwordData, old_password: e.target.value })
                }
                placeholder="Enter old password"
                required
              />
            </div>

            <div className="form-group">
              <label>New Password</label>
              <input
                type="password"
                value={passwordData.new_password}
                onChange={(e) =>
                  setPasswordData({ ...passwordData, new_password: e.target.value })
                }
                placeholder="Enter new password"
                required
              />
            </div>

            <div className="form-group">
              <label>Confirm New Password</label>
              <input
                type="password"
                value={passwordData.confirm_password}
                onChange={(e) =>
                  setPasswordData({ ...passwordData, confirm_password: e.target.value })
                }
                placeholder="Confirm new password"
                required
              />
            </div>

            <button type="submit" className="btn btn-secondary">
              Update Password
            </button>
            {passwordSuccess && <div className="success-message">{passwordSuccess}</div>}
            {passwordError && <div className="error-message">{passwordError}</div>}
          </form>
        </div>
      </div>
    </div>
  );
}
