export default function StatsCard({ icon: Icon, title, value, subtitle, color = 'primary', trend }) {
  const colorClasses = {
    primary: 'bg-primary-600 text-white',
    success: 'bg-success-600 text-white',
    warning: 'bg-warning-500 text-white',
    danger: 'bg-danger-600 text-white',
    info: 'bg-blue-600 text-white',
  };

  const bgClasses = {
    primary: 'bg-primary-50',
    success: 'bg-success-50',
    warning: 'bg-warning-50',
    danger: 'bg-danger-50',
    info: 'bg-blue-50',
  };

  return (
    <div className="bg-white rounded-xl shadow-soft border border-gray-100 p-6 hover:shadow-medium transition-all duration-200 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className={`p-3 rounded-xl shadow-sm ${colorClasses[color]}`}>
            <Icon className="h-6 w-6" />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
            <p className="text-3xl font-bold text-gray-900">{value}</p>
            {subtitle && <p className="text-xs text-gray-500 mt-1 font-medium">{subtitle}</p>}
          </div>
        </div>

        {trend && (
          <div className={`text-right ${trend.positive ? 'text-success-600' : 'text-danger-600'}`}>
            <div className="text-2xl font-bold">{trend.value}</div>
            <div className="text-xs font-medium">{trend.label}</div>
          </div>
        )}
      </div>
    </div>
  );
}
