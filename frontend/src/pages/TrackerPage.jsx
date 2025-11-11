import { useState } from 'react';
import { Search, CheckCircle, Clock, AlertTriangle, FileText } from 'lucide-react';
import axios from 'axios';

export default function TrackerPage() {
  const [referenceId, setReferenceId] = useState('');
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!referenceId.trim()) {
      setError('Please enter a reference ID');
      return;
    }

    setLoading(true);
    setError('');
    setComplaint(null);

    try {
      const response = await axios.get(`/api/v1/complaints/${referenceId}`);
      setComplaint(response.data);
    } catch (err) {
      setError(err.response?.status === 404 
        ? 'Complaint not found. Please check your reference ID.' 
        : 'Error fetching complaint details.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'resolved':
      case 'closed':
        return <CheckCircle className="h-8 w-8 text-green-500" />;
      case 'under_review':
        return <Clock className="h-8 w-8 text-yellow-500" />;
      default:
        return <AlertTriangle className="h-8 w-8 text-blue-500" />;
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Case Tracker</h1>
        <p className="text-gray-600 mt-1">Track your complaint status using the reference ID</p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <form onSubmit={handleSearch} className="space-y-4">
          <div>
            <label htmlFor="referenceId" className="block text-sm font-medium text-gray-700 mb-2">
              Reference ID
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                id="referenceId"
                value={referenceId}
                onChange={(e) => setReferenceId(e.target.value)}
                placeholder="Enter your reference ID (e.g., CS-A1B2C3D4)"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary flex items-center gap-2"
              >
                <Search className="h-4 w-4" />
                {loading ? 'Searching...' : 'Track'}
              </button>
            </div>
          </div>
        </form>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
      </div>

      {complaint && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              {getStatusIcon(complaint.status)}
              <div>
                <h2 className="text-xl font-semibold text-gray-900">
                  {complaint.reference_id}
                </h2>
                <p className="text-sm text-gray-500">
                  Status: <span className="font-medium capitalize">{complaint.status?.replace('_', ' ')}</span>
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Incident Details</h3>
              <dl className="space-y-2">
                <div>
                  <dt className="text-xs text-gray-500">Type</dt>
                  <dd className="text-sm font-medium text-gray-900 capitalize">
                    {complaint.incident_type?.replace('_', ' ')}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-500">Description</dt>
                  <dd className="text-sm text-gray-900">
                    {complaint.description || 'No description provided'}
                  </dd>
                </div>
                {complaint.amount && (
                  <div>
                    <dt className="text-xs text-gray-500">Amount Lost</dt>
                    <dd className="text-sm font-medium text-gray-900">₹{complaint.amount.toLocaleString()}</dd>
                  </div>
                )}
              </dl>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Tracking Information</h3>
              <dl className="space-y-2">
                <div>
                  <dt className="text-xs text-gray-500">Submitted On</dt>
                  <dd className="text-sm text-gray-900">
                    {new Date(complaint.created_at).toLocaleString()}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-500">Last Updated</dt>
                  <dd className="text-sm text-gray-900">
                    {new Date(complaint.updated_at).toLocaleString()}
                  </dd>
                </div>
                {complaint.portal_case_id && (
                  <div>
                    <dt className="text-xs text-gray-500">Portal Case ID</dt>
                    <dd className="text-sm font-medium text-primary-600">
                      {complaint.portal_case_id}
                    </dd>
                  </div>
                )}
              </dl>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
              <FileText className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-blue-800">
                <p className="font-medium mb-1">What's next?</p>
                <p>Your complaint is being reviewed by the cybercrime authorities. You will be contacted if additional information is needed. For urgent assistance, call the helpline at 1930.</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
