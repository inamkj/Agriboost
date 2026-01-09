
import { Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";

import Layout from "./components/Layout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import About from "./pages/About";
import Disease from "./pages/Disease";
import IoT from "./pages/Iot";
import ProfileHistory from "./pages/ProfileHistory";
import CropHistory from "./pages/CropHistory";
import Settings from "./pages/Settings";
import ProtectedRoute from "./components/ProtectedRoute";
import OTPVerification from "./pages/OTPVerification";

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access");
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    setIsLoggedIn(false);
  };

  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} />} />
      <Route path="/register" element={<Register setIsLoggedIn={setIsLoggedIn} />} />
      <Route path="/about" element={<About />} />
      <Route path="/verify-otp" element={<OTPVerification />} />

      {/* Protected Routes with shared Layout */}
      <Route
        element={
          <ProtectedRoute isLoggedIn={isLoggedIn}>
            <Layout handleLogout={handleLogout} />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/disease" element={<Disease />} />
        <Route path="/iot" element={<IoT />} />
        <Route path="/history" element={<ProfileHistory />} />
        <Route path="/crop-history" element={<CropHistory />} />
        <Route path="/settings" element={<Settings />} />
      </Route>

      {/* Catch All */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
