
import '../styles/cropDisease.css';
import { useEffect, useState } from "react";
import axios from "axios";

export default function CropHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const token = localStorage.getItem("access");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/disease/crop-history/",
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setHistory(response.data);
      } catch (error) {
        console.error("Failed to fetch history:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) return <p className="loading">Loading history...</p>;
  if (history.length === 0) return <p className="no-history">No disease history found.</p>;

  return (
    <div className="history-page">
      <h1>Disease History</h1>
      <div className="history-grid">
        {history.map((item) => (
          <div key={item.id} className="history-card">
            <div className="history-info">
              <h3 className="disease-name">{item.label}</h3>
              <p className="confidence">
                <strong>Confidence:</strong> {(item.confidence * 100).toFixed(2)}%
              </p>
              <p className="recommendation">
                <strong>Recommendation:</strong> {item.recommendation}
              </p>
            </div>
            <div className="history-footer">
              <span>{new Date(item.created_at).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
