// import { useState, useEffect } from 'react';
// import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from "recharts";
// import '../styles/main.css';
// import '../styles/iot.css';

// export default function IoTChart({ sensorData }) {
//   const [chartData, setChartData] = useState([]);

//   // Update chart data when sensor data changes
//   useEffect(() => {
//     if (sensorData) {
//       const timestamp = new Date().toLocaleTimeString('en-US', { 
//         hour: '2-digit', 
//         minute: '2-digit' 
//       });
      
//       const newDataPoint = {
//         time: timestamp,
//         temperature: sensorData.temperature || 0,
//         humidity: sensorData.humidity || 0,
//         moisture: sensorData.soil_moisture || 0,
//         ph: sensorData.soil_ph || 0,
//         ec: sensorData.ec || 0,
//         nitrogen: sensorData.nitrogen || 0,
//         phosphorus: sensorData.phosphorus || 0,
//         potassium: sensorData.potassium || 0,
//       };

//       setChartData(prev => {
//         const updated = [...prev, newDataPoint];
//         // Keep only last 20 data points to avoid clutter
//         return updated.slice(-20);
//       });
//     }
//   }, [sensorData]);

//   // Initialize with sample data if no real data yet
//   useEffect(() => {
//     if (chartData.length === 0 && !sensorData) {
//       const sampleData = [
//         { time: "10:00", moisture: 60, ph: 7, nitrogen: 40, phosphorus: 20, potassium: 35 },
//         { time: "11:00", moisture: 65, ph: 6.8, nitrogen: 42, phosphorus: 22, potassium: 37 },
//         { time: "12:00", moisture: 58, ph: 6.9, nitrogen: 39, phosphorus: 21, potassium: 34 },
//       ];
//       setChartData(sampleData);
//     }
//   }, [chartData.length, sensorData]);

//   const data = chartData.length > 0 ? chartData : [];

//   return (
//     <div className="iot-sensor-card" style={{ marginTop: '24px' }}>
//       <h3>Real-time Sensor Data Trends</h3>
//       <p>Historical data visualization of all sensor readings over time.</p>
//       <ResponsiveContainer width="100%" height={350}>
//         <LineChart data={data}>
//           <CartesianGrid strokeDasharray="3 3" />
//           <XAxis 
//             dataKey="time" 
//             label={{ value: 'Time', position: 'insideBottom', offset: -5 }}
//           />
//           <YAxis 
//             yAxisId="left"
//             label={{ value: 'Values', angle: -90, position: 'insideLeft' }}
//           />
//           <Tooltip 
//             contentStyle={{ 
//               backgroundColor: '#fff', 
//               border: '1px solid #ccc',
//               borderRadius: '8px'
//             }}
//           />
//           <Legend 
//             wrapperStyle={{ paddingTop: '20px' }}
//           />

//           {/* Environmental Data */}
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="temperature" 
//             stroke="#e74c3c" 
//             strokeWidth={2}
//             name="Temperature (°C)"
//             dot={{ r: 3 }}
//           />
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="humidity" 
//             stroke="#3498db" 
//             strokeWidth={2}
//             name="Humidity (%)"
//             dot={{ r: 3 }}
//           />
          
//           {/* Soil Data */}
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="moisture" 
//             stroke="#4caf50" 
//             strokeWidth={2}
//             name="Soil Moisture (%)"
//             dot={{ r: 3 }}
//           />
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="ph" 
//             stroke="#2196f3" 
//             strokeWidth={2}
//             name="pH"
//             dot={{ r: 3 }}
//           />
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="ec" 
//             stroke="#ff9800" 
//             strokeWidth={2}
//             name="EC"
//             dot={{ r: 3 }}
//           />

//           {/* NPK Lines */}
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="nitrogen" 
//             stroke="#ff5722" 
//             strokeWidth={2}
//             name="Nitrogen (N)"
//             dot={{ r: 3 }}
//           />
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="phosphorus" 
//             stroke="#9c27b0" 
//             strokeWidth={2}
//             name="Phosphorus (P)"
//             dot={{ r: 3 }}
//           />
//           <Line 
//             yAxisId="left"
//             type="monotone" 
//             dataKey="potassium" 
//             stroke="#ffc107" 
//             strokeWidth={2}
//             name="Potassium (K)"
//             dot={{ r: 3 }}
//           />
//         </LineChart>
//       </ResponsiveContainer>
      
//       {data.length === 0 && (
//         <div className="iot-loading" style={{ padding: '20px' }}>
//           <p style={{ textAlign: 'center', color: '#718096' }}>
//             Waiting for sensor data...
//           </p>
//         </div>
//       )}
//     </div>
//   );
// }
import { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer
} from "recharts";
import '../styles/main.css';
import '../styles/iot.css';

export default function IoTChart({ sensorData }) {
  const [chartData, setChartData] = useState([]);

  // Update chart with real-time data
  useEffect(() => {
    if (sensorData) {
      const timestamp = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      });

      const newPoint = {
        time: timestamp,
        temperature: sensorData.temperature || 0,
        humidity: sensorData.humidity || 0,
        moisture: sensorData.soil_moisture || 0,
        ph: sensorData.soil_ph || 0,
        ec: sensorData.ec || 0,
        nitrogen: sensorData.nitrogen || 0,
        phosphorus: sensorData.phosphorus || 0,
        potassium: sensorData.potassium || 0
      };

      setChartData(prev => [...prev.slice(-19), newPoint]);
    }
  }, [sensorData]);

  const data = chartData;

  return (
    <div className="iot-sensor-card" style={{ marginTop: '24px', padding: '20px', borderRadius: '16px', background: '#fff', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
      <h3 style={{ marginBottom: '8px' }}>Real-time Sensor Data Trends</h3>
      <p style={{ color: '#666', marginBottom: '20px' }}>Visualizing environmental and soil metrics together in one chart.</p>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          {/* Grid */}
          <CartesianGrid stroke="#e0e0e0" strokeDasharray="4 4" />

          {/* X-Axis */}
          <XAxis dataKey="time" stroke="#333" tick={{ fontSize: 12 }} />

          {/* Y-Axis */}
          <YAxis stroke="#333" tick={{ fontSize: 12 }} />

          {/* Tooltip */}
          <Tooltip 
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px' }} 
          />

          {/* Legend */}
          <Legend verticalAlign="bottom" height={36} />

          {/* Lines */}
          <Line type="monotone" dataKey="temperature" stroke="#e74c3c" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Temperature (°C)" />
          <Line type="monotone" dataKey="humidity" stroke="#3498db" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Humidity (%)" />
          <Line type="monotone" dataKey="moisture" stroke="#4caf50" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Soil Moisture (%)" />
          <Line type="monotone" dataKey="ph" stroke="#2196f3" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="pH" />
          <Line type="monotone" dataKey="ec" stroke="#ff9800" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="EC" />
          <Line type="monotone" dataKey="nitrogen" stroke="#ff5722" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Nitrogen (N)" />
          <Line type="monotone" dataKey="phosphorus" stroke="#9c27b0" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Phosphorus (P)" />
          <Line type="monotone" dataKey="potassium" stroke="#ffc107" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} name="Potassium (K)" />
        </LineChart>
      </ResponsiveContainer>

      {data.length === 0 && (
        <p style={{ textAlign: 'center', marginTop: '20px', color: '#718096' }}>
          Waiting for sensor data…
        </p>
      )}
    </div>
  );
}
