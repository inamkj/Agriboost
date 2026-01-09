import React from "react";
import { CircleLoader } from "react-spinners";
import "../styles/LoaderOverlay.css";

export default function LoaderOverlay({ loading, message = "Loading..." }) {
  if (!loading) return null;

  return (
    <div className="loader-overlay">
      <div className="loader-box">
        <CircleLoader size={80} color="#4CAF50" />
        <p>{message}</p>
      </div>
    </div>
  );
}
