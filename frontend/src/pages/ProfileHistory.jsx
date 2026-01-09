import "../styles/profile.css";
import { useEffect, useState } from "react";
import api from "../axios";

export default function ProfileHistory() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError("");
    api
      .get("/users/history/")
      .then((res) => {
        if (!isMounted) return;
        setItems(res.data);
      })
      .catch((err) => {
        if (!isMounted) return;
        const msg = err.response?.data?.detail || "Failed to load history.";
        setError(msg);
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });
    return () => {
      isMounted = false;
    };
  }, []);

  return (
     <div className="history-card">
      <h3>User History</h3>
      {loading && <p className="loading">Loading…</p>}
      {error && <p className="error-message">{error}</p>}
      {!loading && !error && (
        <ul className="history-list">
          {items.length === 0 && <li className="empty">No activities yet.</li>}
          {items.map((h) => {
            let details = null;
            try {
              details = h.details ? JSON.parse(h.details) : null;
            } catch (e) {
              details = null;
            }
            return (
              <li key={h.id} className="history-item">
                <div className="history-time">
                  {new Date(h.created_at).toLocaleString()}
                </div>
                <div className="history-content">
                  <span className="history-action">{h.action}</span>
                  {h.description && (
                    <span className="history-description">
                      {" — "}{h.description}
                    </span>
                  )}
                  {details && (
                    <div className="history-details">
                      {details.changed &&
                        Object.keys(details.changed).map((k) => (
                          <div key={k}>
                            {k}: {details.changed[k].from} → {details.changed[k].to}
                          </div>
                        ))}
                      {details.ip && <div>IP: {details.ip}</div>}
                    </div>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
