import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";
import '../styles/crophealthchart.css';

const healthData = [
  { day: "Mon", score: 78 },
  { day: "Tue", score: 82 },
  { day: "Wed", score: 76 },
  { day: "Thu", score: 85 },
  { day: "Fri", score: 80 },
];

const npkData = [
  { nutrient: "Nitrogen", value: 60 },
  { nutrient: "Phosphorus", value: 45 },
  { nutrient: "Potassium", value: 70 },
];

const diseaseData = [
  { status: "Healthy", value: 85 },
  { status: "Diseased", value: 15 },
];

const COLORS = ["#4caf50", "#f44336"];

export default function CropHealthCharts() {
  return (
    <div className="charts-container">
      {/* Line Chart */}
      <div className="chart-card">
        <h3>Crop Health Score (Last 5 Days)</h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={healthData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke="#4caf50" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Bar Chart */}
      <div className="chart-card">
        <h3>Soil Nutrients (NPK)</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={npkData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="nutrient" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#218838" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pie Chart */}
      <div className="chart-card">
        <h3>Crop Health Status</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={diseaseData}
              dataKey="value"
              nameKey="status"
              cx="50%"
              cy="50%"
              outerRadius={90}
              label
            >
              {diseaseData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Legend />
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
