import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Download, Calendar } from 'lucide-react';

export default function AnalyticsPage() {
  const complaintsOverTime = [
    { month: 'Jun', complaints: 65 },
    { month: 'Jul', complaints: 89 },
    { month: 'Aug', complaints: 102 },
    { month: 'Sep', complaints: 95 },
    { month: 'Oct', complaints: 112 },
    { month: 'Nov', complaints: 128 },
  ];

  const scamTypeData = [
    { name: 'UPI Fraud', value: 340, color: '#4F46E5' },
    { name: 'Job Fraud', value: 280, color: '#7C3AED' },
    { name: 'Online Shopping', value: 220, color: '#EC4899' },
    { name: 'Lottery Scam', value: 180, color: '#F59E0B' },
    { name: 'Others', value: 120, color: '#10B981' },
  ];

  const districtData = [
    { district: 'Khordha', count: 145 },
    { district: 'Cuttack', count: 132 },
    { district: 'Puri', count: 98 },
    { district: 'Ganjam', count: 87 },
    { district: 'Balasore', count: 76 },
  ];

  const languageData = [
    { name: 'English', value: 45 },
    { name: 'Hindi', value: 30 },
    { name: 'Odia', value: 25 },
  ];

  const COLORS = ['#4F46E5', '#7C3AED', '#EC4899'];

  const stats = [
    { label: 'Total Complaints', value: '1,247', change: '+12%', trend: 'up' },
    { label: 'Resolved Cases', value: '892', change: '+8%', trend: 'up' },
    { label: 'Avg Resolution Time', value: '4.2 days', change: '-15%', trend: 'down' },
    { label: 'Total Recovery', value: '₹12.5L', change: '+22%', trend: 'up' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="text-gray-600 mt-1">Comprehensive insights and trends</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            Last 30 Days
          </button>
          <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center gap-2">
            <Download className="h-4 w-4" />
            Export Report
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-xl shadow-lg p-6">
            <p className="text-sm text-gray-600 mb-1">{stat.label}</p>
            <div className="flex items-baseline justify-between">
              <h3 className="text-3xl font-bold text-gray-900">{stat.value}</h3>
              <div
                className={`flex items-center text-sm font-semibold ${
                  stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {stat.trend === 'up' ? (
                  <TrendingUp className="h-4 w-4 mr-1" />
                ) : (
                  <TrendingDown className="h-4 w-4 mr-1" />
                )}
                {stat.change}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Complaints Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={complaintsOverTime}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="complaints" stroke="#4F46E5" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Scam Type Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={scamTypeData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {scamTypeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Top Districts by Complaints</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={districtData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="district" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Language Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={languageData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {languageData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
