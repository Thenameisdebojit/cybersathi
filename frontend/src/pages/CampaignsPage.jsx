import { useState } from 'react';
import { Plus, Send, Calendar, Users, MessageSquare, Edit, Trash2 } from 'lucide-react';

export default function CampaignsPage() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newCampaign, setNewCampaign] = useState({
    title: '',
    message: '',
    targetAudience: 'all',
    district: 'all',
    language: 'all',
    scheduleDate: '',
  });

  const campaigns = [
    {
      id: 1,
      title: 'UPI Fraud Awareness',
      message: 'Never share your UPI PIN with anyone. Banks never ask for PIN...',
      audience: 'All Users',
      district: 'All Districts',
      language: 'English, Hindi, Odia',
      status: 'sent',
      sentDate: '2024-11-10',
      recipients: 1247,
    },
    {
      id: 2,
      title: 'Job Scam Alert',
      message: 'Beware of fake job offers asking for upfront payment...',
      audience: 'All Users',
      district: 'Khordha',
      language: 'Odia',
      status: 'scheduled',
      sentDate: '2024-11-15',
      recipients: 340,
    },
    {
      id: 3,
      title: 'Online Shopping Safety',
      message: 'Always verify seller credentials before making payments...',
      audience: 'All Users',
      district: 'All Districts',
      language: 'English',
      status: 'draft',
      sentDate: null,
      recipients: 0,
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'sent':
        return 'bg-green-100 text-green-800';
      case 'scheduled':
        return 'bg-blue-100 text-blue-800';
      case 'draft':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleCreateCampaign = (e) => {
    e.preventDefault();
    alert('Creating campaign: ' + newCampaign.title);
    setShowCreateModal(false);
    setNewCampaign({
      title: '',
      message: '',
      targetAudience: 'all',
      district: 'all',
      language: 'all',
      scheduleDate: '',
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Awareness Campaigns</h1>
          <p className="text-gray-600 mt-1">Create and manage awareness broadcasts</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-2"
        >
          <Plus className="h-5 w-5" />
          Create Campaign
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">Total Campaigns</h3>
            <Send className="h-5 w-5 text-indigo-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">24</p>
          <p className="text-xs text-gray-500 mt-1">+3 this month</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">Total Recipients</h3>
            <Users className="h-5 w-5 text-green-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">12,847</p>
          <p className="text-xs text-gray-500 mt-1">Across all campaigns</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-medium text-gray-600">Scheduled</h3>
            <Calendar className="h-5 w-5 text-blue-600" />
          </div>
          <p className="text-3xl font-bold text-gray-900">3</p>
          <p className="text-xs text-gray-500 mt-1">Upcoming broadcasts</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Campaign List</h2>
        </div>

        <div className="divide-y divide-gray-200">
          {campaigns.map((campaign) => (
            <div key={campaign.id} className="p-6 hover:bg-gray-50 transition">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{campaign.title}</h3>
                    <span
                      className={`px-3 py-1 text-xs font-semibold rounded-full ${getStatusColor(
                        campaign.status
                      )}`}
                    >
                      {campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{campaign.message}</p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Target:</span>
                      <p className="font-medium text-gray-900">{campaign.audience}</p>
                    </div>
                    <div>
                      <span className="text-gray-500">District:</span>
                      <p className="font-medium text-gray-900">{campaign.district}</p>
                    </div>
                    <div>
                      <span className="text-gray-500">Language:</span>
                      <p className="font-medium text-gray-900">{campaign.language}</p>
                    </div>
                    <div>
                      <span className="text-gray-500">Recipients:</span>
                      <p className="font-medium text-gray-900">{campaign.recipients}</p>
                    </div>
                  </div>
                </div>

                <div className="flex gap-2 ml-4">
                  <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition">
                    <Edit className="h-5 w-5" />
                  </button>
                  <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition">
                    <Trash2 className="h-5 w-5" />
                  </button>
                </div>
              </div>

              {campaign.sentDate && (
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Calendar className="h-4 w-4" />
                  {campaign.status === 'sent' ? 'Sent on' : 'Scheduled for'}: {campaign.sentDate}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
              <h2 className="text-2xl font-bold text-white">Create New Campaign</h2>
            </div>

            <form onSubmit={handleCreateCampaign} className="p-6 space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Campaign Title
                </label>
                <input
                  type="text"
                  required
                  value={newCampaign.title}
                  onChange={(e) => setNewCampaign({ ...newCampaign, title: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                  placeholder="e.g., UPI Fraud Awareness"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Message Content
                </label>
                <textarea
                  required
                  rows="4"
                  value={newCampaign.message}
                  onChange={(e) => setNewCampaign({ ...newCampaign, message: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                  placeholder="Enter your awareness message..."
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">District</label>
                  <select
                    value={newCampaign.district}
                    onChange={(e) => setNewCampaign({ ...newCampaign, district: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                  >
                    <option value="all">All Districts</option>
                    <option value="khordha">Khordha</option>
                    <option value="cuttack">Cuttack</option>
                    <option value="puri">Puri</option>
                    <option value="ganjam">Ganjam</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
                  <select
                    value={newCampaign.language}
                    onChange={(e) => setNewCampaign({ ...newCampaign, language: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                  >
                    <option value="all">All Languages</option>
                    <option value="english">English</option>
                    <option value="hindi">Hindi</option>
                    <option value="odia">Odia</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Schedule Date (Optional)
                </label>
                <input
                  type="datetime-local"
                  value={newCampaign.scheduleDate}
                  onChange={(e) =>
                    setNewCampaign({ ...newCampaign, scheduleDate: e.target.value })
                  }
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
                />
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-2 font-medium"
                >
                  <Send className="h-5 w-5" />
                  {newCampaign.scheduleDate ? 'Schedule Campaign' : 'Send Now'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
