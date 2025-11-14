import { useState } from 'react';
import { Filter, X, Calendar, MapPin, Search, RotateCcw } from 'lucide-react';

export default function FiltersPanel({ filters, onFiltersChange, onReset }) {
  const [isOpen, setIsOpen] = useState(false);

  const statusOptions = [
    { value: '', label: 'All Statuses' },
    { value: 'registered', label: 'New' },
    { value: 'under_review', label: 'In Progress' },
    { value: 'resolved', label: 'Resolved' },
    { value: 'closed', label: 'Closed' },
    { value: 'escalated', label: 'Escalated' },
  ];

  const complaintTypes = [
    { value: '', label: 'All Types' },
    { value: 'online_fraud', label: 'Online Fraud' },
    { value: 'cyber_bullying', label: 'Cyber Bullying' },
    { value: 'hacking', label: 'Hacking' },
    { value: 'identity_theft', label: 'Identity Theft' },
    { value: 'phishing', label: 'Phishing' },
    { value: 'ransomware', label: 'Ransomware' },
    { value: 'other', label: 'Other' },
  ];

  const handleChange = (field, value) => {
    onFiltersChange({ ...filters, [field]: value });
  };

  const handleReset = () => {
    onReset();
    setIsOpen(false);
  };

  const activeFilterCount = Object.values(filters || {}).filter(v => v && v !== '').length;

  return (
    <div className="bg-white rounded-xl shadow-soft border border-gray-100 p-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Filter className="h-5 w-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
          {activeFilterCount > 0 && (
            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
              {activeFilterCount} active
            </span>
          )}
        </div>
        <button
          onClick={handleReset}
          className="text-sm font-medium text-gray-600 hover:text-primary-600 flex items-center gap-1 transition-colors"
        >
          <RotateCcw className="h-4 w-4" />
          Reset
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Search className="h-4 w-4 inline mr-1" />
            Search Ticket
          </label>
          <input
            type="text"
            placeholder="CS-20241114-XXXXXX"
            value={filters?.ticket_id || ''}
            onChange={(e) => handleChange('ticket_id', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Status
          </label>
          <select
            value={filters?.status || ''}
            onChange={(e) => handleChange('status', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          >
            {statusOptions.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Complaint Type
          </label>
          <select
            value={filters?.complaint_type || ''}
            onChange={(e) => handleChange('complaint_type', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          >
            {complaintTypes.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="h-4 w-4 inline mr-1" />
            District
          </label>
          <input
            type="text"
            placeholder="Enter district"
            value={filters?.district || ''}
            onChange={(e) => handleChange('district', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Calendar className="h-4 w-4 inline mr-1" />
            From Date
          </label>
          <input
            type="date"
            value={filters?.from_date || ''}
            onChange={(e) => handleChange('from_date', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Calendar className="h-4 w-4 inline mr-1" />
            To Date
          </label>
          <input
            type="date"
            value={filters?.to_date || ''}
            onChange={(e) => handleChange('to_date', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Mobile Number
          </label>
          <input
            type="text"
            placeholder="Enter mobile"
            value={filters?.mobile || ''}
            onChange={(e) => handleChange('mobile', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Citizen Name
          </label>
          <input
            type="text"
            placeholder="Enter name"
            value={filters?.name || ''}
            onChange={(e) => handleChange('name', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
        </div>
      </div>
    </div>
  );
}
