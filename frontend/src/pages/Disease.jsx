import "../styles/main.css";
import { useState } from "react";
import api from "../axios";

export default function Disease() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return setError("Please select an image first.");
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const form = new FormData();
      form.append("image", file);
      const res = await api.post("/disease/predict/", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(res.data?.prediction || null);
    } catch (e) {
      const msg =
        e.response?.data?.detail ||
        e.response?.data?.image ||
        "Prediction failed.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  // Determine confidence bar color
  const getConfidenceColor = (conf) => {
    if (conf > 0.8) return "confidence-high";
    if (conf > 0.5) return "confidence-medium";
    return "confidence-low";
  };

  return (
    <div className="card">
      <h3>Disease Detection</h3>
      <p>Upload an image of your sugarcane crop to detect diseases using AI.</p>

      {/* File input */}
      <div className="file-upload-wrapper">
        <label htmlFor="file-upload" className="file-label">
          📷 Choose Image
        </label>
        <input
          id="file-upload"
          type="file"
          className="file-input-hidden"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        {file && <span className="file-name">{file.name}</span>}
      </div>

      {/* Upload button */}
      <button className="btn" onClick={handleUpload} disabled={loading}>
        {loading ? "Predicting..." : "Detect Now"}
      </button>

      {/* Error */}
      {error && <p className="error-message">{error}</p>}

      {/* Result */}
      {result && (
        <div className="result-box">
          <h4>Prediction Result</h4>

          {/* Disease Badge */}
          <div className="result-badge">
            <span
              className={`disease-badge ${
                result.label === "Healthy" ? "badge-healthy" : "badge-disease"
              }`}
            >
              {result.label}
            </span>
          </div>

          {/* Confidence Bar */}
          <div className="confidence-wrapper">
            <div className="confidence-text">
              Confidence: {Math.round((result.confidence || 0) * 100)}%
            </div>
            <div className="confidence-bar">
              <div
                className={`confidence-fill ${getConfidenceColor(
                  result.confidence
                )}`}
                style={{
                  width: `${Math.round((result.confidence || 0) * 100)}%`,
                }}
              />
            </div>
          </div>

          {/* Recommendation */}
          <div className="recommendation-box">
            <strong>Recommendation:</strong>
            <p>{result.recommendation}</p>
          </div>
        </div>
      )}
    </div>
  );
}
