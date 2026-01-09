import { useState, useEffect } from 'react';
import "../styles/main.css";
import "../styles/iot.css";
import IoTChart from '../components/IotChart';
import api from '../axios';

export default function IoT() {
  const [sensorData, setSensorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [dataSource, setDataSource] = useState('placeholder');
  const [prediction, setPrediction] = useState(null);
  const [predicting, setPredicting] = useState(false);
  const [predictionHistory, setPredictionHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [soilType, setSoilType] = useState("");

  // Fetch sensor data from API
  const fetchSensorData = async () => {
    try {
      setError(null);
      const response = await api.get('/sensors/feed/');
      const data = response.data;
      
      if (data.sensors && data.sensors.length > 0) {
        setSensorData(data.sensors[0]); // Get first sensor
        setLastUpdated(data.last_updated);
        setDataSource(data.source || 'unknown');
      }
    } catch (err) {
      console.error('Error fetching sensor data:', err);
      setError('Failed to fetch sensor data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch prediction history (only if authenticated)
  const fetchPredictionHistory = async () => {
    try {
      const token = localStorage.getItem('access');
      if (!token) {
        // User not authenticated, skip fetching history
        return;
      }
      const response = await api.get('/sensors/predictions/');
      setPredictionHistory(response.data.results || []);
    } catch (err) {
      // Silently fail if not authenticated or other error
      console.error('Error fetching prediction history:', err);
    }
  };

  // Predict fertilizer based on current sensor readings
  const handlePredictFertilizer = async () => {
    if (!sensorData) {
    setError('No sensor data available for prediction.');
    return;
  }
  
  if (!soilType) {
    setError('Please select a soil type before predicting.');
    return;
  }

  setPredicting(true);
  setError(null);

    setPredicting(true);
    setError(null);

    try {
      // Send current sensor readings to prediction endpoint
      // No body needed - endpoint will use current Firebase readings
      // const response = await api.post('/sensors/predict/');
              const response = await api.post('/sensors/predict/', {
    temperature: sensorData.temperature,
    humidity: sensorData.humidity,
    moisture: sensorData.soil_moisture,
    crop_type: "Sugarcane",
    soil_type: soilType, // matches serializer
    nitrogen: sensorData.nitrogen,
    potassium: sensorData.potassium,
    phosphorous: sensorData.phosphorous,  // corrected spelling
    
     // from dropdown
});
      setPrediction(response.data.prediction);
      
      // Refresh history
      await fetchPredictionHistory();
      
      // Scroll to prediction result
      setTimeout(() => {
        const resultElement = document.getElementById('prediction-result');
        if (resultElement) {
          resultElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
    } catch (err) {
      console.error('Error predicting fertilizer:', err);
      if (err.response?.status === 401) {
        setError('Please login to save fertilizer predictions. Predictions require authentication.');
      } else {
        setError(err.response?.data?.error || err.response?.data?.detail || 'Failed to predict fertilizer. Please try again.');
      }
    } finally {
      setPredicting(false);
    }
  };

  // Initial fetch and set up polling (every 5 seconds)
  useEffect(() => {
    fetchSensorData();
    fetchPredictionHistory();
    
    // Set up interval to fetch data every 5 seconds for real-time updates
    const interval = setInterval(() => {
      fetchSensorData();
    }, 5000); // Update every 5 seconds

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  // Format timestamp for display
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'N/A';
    try {
      const date = new Date(timestamp);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    } catch {
      return timestamp;
    }
  };

  if (loading && !sensorData) {
    return (
      <div className="iot-container">
        <div className="iot-loading">
          <div className="iot-loading-spinner"></div>
          <p>Loading sensor data...</p>
        </div>
      </div>
    );
  }

  const sensor = sensorData || {};

  return (
    <div className="iot-container">
      {/* Status indicator */}
      <div className={`iot-status-card ${dataSource === 'firebase' ? '' : 'placeholder'}`}>
        <div className="iot-status-indicator">
          <span className={`iot-status-dot ${dataSource === 'firebase' ? '' : 'placeholder'}`}></span>
          <span className="iot-status-text">
            {dataSource === 'firebase' ? 'Live Data (Firebase)' : 'Placeholder Data'}
          </span>
        </div>
        {lastUpdated && (
          <span className="iot-status-time">
            Last updated: {formatTimestamp(lastUpdated)}
          </span>
        )}
      </div>

      {/* Main Sensor Readings Card */}
      <div className="iot-sensor-card">
        <h3>Sensor Readings</h3>
        <p>Live data from IoT devices monitoring soil and environment.</p>
        
        {error && (
          <div className="iot-error">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {sensorData && (
          <>
            <div className="iot-sensor-grid">
              {/* Temperature */}
              <div className="iot-sensor-item temperature">
                
                <div className="iot-sensor-label">Temperature</div>
                <div className="iot-sensor-value">
                  {sensor.temperature?.toFixed(1) || 'N/A'}°C
                </div>
              </div>

              {/* Humidity */}
              <div className="iot-sensor-item humidity">
                
                <div className="iot-sensor-label">Humidity</div>
                <div className="iot-sensor-value">
                  {sensor.humidity?.toFixed(1) || 'N/A'}%
                </div>
              </div>

              {/* Soil Moisture */}
              <div className="iot-sensor-item moisture">
                <div className="iot-sensor-label">Soil Moisture</div>
                <div className="iot-sensor-value">
                  {sensor.soil_moisture?.toFixed(1) || 'N/A'}%
                </div>
              </div>

              {/* Soil pH */}
              <div className="iot-sensor-item ph">
                <div className="iot-sensor-label">Soil pH</div>
                <div className="iot-sensor-value">
                  {sensor.soil_ph?.toFixed(2) || 'N/A'}
                </div>
              </div>

              {/* Electrical Conductivity */}
              <div className="iot-sensor-item ec">
                <div className="iot-sensor-label">EC</div>
                <div className="iot-sensor-value">
                  {sensor.ec?.toFixed(2) || 'N/A'}
                </div>
              </div>

              {/* Battery */}
              <div className={`iot-sensor-item battery ${sensor.battery <= 20 ? 'low' : ''}`}>
                <div className="iot-sensor-label">Battery</div>
                <div className="iot-sensor-value">
                  {sensor.battery?.toFixed(1) || 'N/A'}%
                </div>
              </div>
            </div>

            {/* NPK Values */}
            <div className="iot-npk-section">
              <h4>NPK Values</h4>
              <div className="iot-npk-grid">
                <div className="iot-npk-item nitrogen">
                  <div className="iot-npk-label">Nitrogen (N)</div>
                  <div className="iot-npk-value">
                    {sensor.nitrogen?.toFixed(1) || 'N/A'}
                  </div>
                </div>
                <div className="iot-npk-item phosphorus">
                  <div className="iot-npk-label">Phosphorus (P)</div>
                  <div className="iot-npk-value">
                    {sensor.phosphorous?.toFixed(1) || 'N/A'}
                  </div>
                </div>
                <div className="iot-npk-item potassium">
                  <div className="iot-npk-label">Potassium (K)</div>
                  <div className="iot-npk-value">
                    {sensor.potassium?.toFixed(1) || 'N/A'}
                  </div>
                </div>
              </div>
            </div>

            {/* Alerts */}
            {sensor.alerts && sensor.alerts.length > 0 && (
              <div className="iot-alerts-section">
                <h4>
                  <span>⚠️</span>
                  <span>Alerts & Warnings</span>
                </h4>
                <div className="iot-alerts-list">
                  {sensor.alerts.map((alert, index) => {
                    const isHigh = alert.toLowerCase().includes('high') || alert.toLowerCase().includes('exceeds');
                    const isLow = alert.toLowerCase().includes('low') || alert.toLowerCase().includes('below');
                    return (
                      <div 
                        key={index}
                        className={`iot-alert ${isHigh ? 'high' : isLow ? 'low' : 'warning'}`}
                      >
                        <span className="iot-alert-icon">
                          {isHigh ? '🔴' : isLow ? '🟡' : '⚠️'}
                        </span>
                        <span>{alert}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Predict Fertilizer Section */}
            <div className="iot-predict-section">
              <select 
  value={soilType}
  onChange={(e) => setSoilType(e.target.value)}
  className="form-control"
>
  <option value="">Select Soil Type</option>
  <option value="Loamy">Loamy</option>
  <option value="Clayey">Clayey</option>
  <option value="Sandy">Sandy</option>
  <option value="Black">Black</option>
  <option value="Red">Red</option>
</select>

              <button
                className={`iot-predict-button ${predicting ? 'loading' : ''}`}
                onClick={handlePredictFertilizer}
                disabled={predicting || !sensorData}
              >
                {predicting ? (
                  <>
                    <span className="iot-loading-spinner" style={{ width: '20px', height: '20px', borderWidth: '2px' }}></span>
                    <span>Predicting...</span>
                  </>
                ) : (
                  <>
                    
                    <span>Predict Fertilizer</span>
                  </>
                )}
              </button>

              {/* Prediction Result */}
              {prediction && (
                <div id="prediction-result" className="iot-prediction-result">
                  <h4>
                    <span>🌱</span>
                    <span>Fertilizer Recommendation</span>
                  </h4>
                  <div className="iot-prediction-details">
                    <div className="iot-prediction-detail">
                      <div className="iot-prediction-detail-label">Recommended Fertilizer</div>
                      <div className="iot-prediction-detail-value">{prediction.recommended_fertilizer}</div>
                    </div>
                    {prediction.fertilizer_amount && (
                      <div className="iot-prediction-detail">
                        <div className="iot-prediction-detail-label">Amount</div>
                        <div className="iot-prediction-detail-value">{prediction.fertilizer_amount} kg/hectare</div>
                      </div>
                    )}
                    {prediction.confidence_score && (
                      <div className="iot-prediction-detail">
                        <div className="iot-prediction-detail-label">Confidence</div>
                        <div className="iot-prediction-detail-value">{(prediction.confidence_score * 100).toFixed(0)}%</div>
                      </div>
                    )}
                  </div>

                  {/* Instructions Section */}
                  {prediction.instructions && (
                    <div className="iot-instructions-section" style={{ marginTop: '20px' }}>
                      <h5 className="iot-section-title">
                        <span>📋</span>
                        <span>Application Instructions</span>
                      </h5>
                      <div className="iot-instructions-content">
                        {prediction.instructions.split('\n').filter(line => line.trim()).map((line, idx) => (
                          <div key={idx} className="iot-instruction-line">
                            {line.trim()}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Precautions Section */}
                  {prediction.precautions && (
                    <div className="iot-precautions-section" style={{ marginTop: '20px' }}>
                      <h5 className="iot-section-title">
                        <span>⚠️</span>
                        <span>Safety Precautions</span>
                      </h5>
                      <div className="iot-precautions-content">
                        {prediction.precautions.split('\n').filter(line => line.trim()).map((line, idx) => (
                          <div key={idx} className="iot-precaution-line">
                            {line.trim()}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <button
                    onClick={() => setShowHistory(!showHistory)}
                    style={{
                      marginTop: '20px',
                      padding: '10px 20px',
                      background: 'white',
                      border: '2px solid #4caf50',
                      borderRadius: '8px',
                      color: '#2e7d32',
                      cursor: 'pointer',
                      fontWeight: '600',
                      fontSize: '14px',
                      transition: 'all 0.3s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.target.style.background = '#4caf50';
                      e.target.style.color = 'white';
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.background = 'white';
                      e.target.style.color = '#2e7d32';
                    }}
                  >
                    {showHistory ? 'Hide' : 'Show'} Prediction History
                  </button>
                </div>
              )}
            </div>
          </>
        )}
      </div>

      {/* Prediction History */}
      {showHistory && predictionHistory.length > 0 && (
        <div className="iot-sensor-card" style={{ marginTop: '24px' }}>
          <h3>Prediction History</h3>
          <p>Previous fertilizer recommendations based on sensor readings.</p>
          <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {predictionHistory.slice(0, 10).map((pred) => (
              <div
                key={pred.id}
                style={{
                  padding: '16px',
                  background: '#f8f9fa',
                  borderRadius: '10px',
                  border: '1px solid #e5e7eb'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '12px' }}>
                  <div>
                    <div style={{ fontWeight: '600', color: '#2d3748', fontSize: '16px' }}>
                      {pred.recommended_fertilizer}
                    </div>
                    <div style={{ fontSize: '12px', color: '#718096', marginTop: '4px' }}>
                      {formatTimestamp(pred.created_at)}
                    </div>
                  </div>
                  <div style={{ fontSize: '14px', fontWeight: '600', color: '#4caf50' }}>
                    {pred.fertilizer_amount} kg/ha
                  </div>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-3 text-sm text-gray-700">
            <div><span className="font-medium">N:</span> {pred.nitrogen || "-"}</div>
            <div><span className="font-medium">P:</span> {pred.phosphorous || "-"}</div>
            <div><span className="font-medium">K:</span> {pred.potassium || "-"}</div>
            <div><span className="font-medium">Temp:</span> {pred.temperature ? `${pred.temperature}°C` : "-"}</div>
            <div><span className="font-medium">EC:</span> {pred.ec || "-"}</div>
            <div><span className="font-medium">pH:</span> {pred.soil_ph || "-"}</div>
            <div><span className="font-medium">Moisture:</span> {pred.moisture || "-"}</div>
          </div>
                <div style={{ fontSize: '13px', color: '#4a5568', marginTop: '8px' }}>
                  Confidence: {(pred.confidence_score * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Chart Component */}
      <IoTChart sensorData={sensorData} />
    </div>
  );
}


