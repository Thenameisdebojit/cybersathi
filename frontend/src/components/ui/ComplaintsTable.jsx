import { useState } from 'react';
import { Eye, Download, Calendar, MapPin, Phone } from 'lucide-react';
import StatusBadge from './StatusBadge';
import Pagination from './Pagination';
import { Link } from 'react-router-dom';

export default function ComplaintsTable({ complaints = [], onViewDetails, currentPage = 1, totalPages = 1, onPageChange }) {
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const maskPhone = (phone) => {
    if (!phone) return 'N/A';
    return `******${phone.slice(-4)}`;
  };

  if (!complaints || complaints.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-soft p-12 text-center">
        <div className="max-w-sm mx-auto">
          <div className="h-16 w-16 bg-gray-100 rounded-full mx-auto flex items-center justify-center mb-4">
            <Eye className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Complaints Found</h3>
          <p className="text-gray-600 text-sm">
            No complaints match your current filters. Try adjusting your search criteria.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-soft border border-gray-100 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Ticket ID
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Citizen Details
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Complaint Type
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Location
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Date Filed
              </th>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-4 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {complaints.map((complaint) => (
              <tr key={complaint._id || complaint.ticket_id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    <div className="text-sm font-mono font-bold text-primary-600">
                      {complaint.ticket_id}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm">
                    <div className="font-medium text-gray-900">{complaint.name || 'N/A'}</div>
                    <div className="text-gray-500 flex items-center gap-1 mt-1">
                      <Phone className="h-3 w-3" />
                      {maskPhone(complaint.mobile)}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm">
                    <div className="font-medium text-gray-900">
                      {complaint.complaint_type || 'General'}
                    </div>
                    {complaint.subcategory && (
                      <div className="text-xs text-gray-500 mt-1">{complaint.subcategory}</div>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-600 flex items-center gap-1">
                    <MapPin className="h-3 w-3" />
                    <span>{complaint.district || 'N/A'}</span>
                  </div>
                  {complaint.police_station && (
                    <div className="text-xs text-gray-500 mt-1">PS: {complaint.police_station}</div>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-600 flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    {formatDate(complaint.created_at)}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <StatusBadge status={complaint.status || 'registered'} />
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex items-center justify-end gap-2">
                    <Link
                      to={`/complaints/${complaint._id || complaint.ticket_id}`}
                      className="inline-flex items-center gap-1 px-3 py-1.5 bg-primary-50 text-primary-700 rounded-lg hover:bg-primary-100 transition-colors font-medium"
                    >
                      <Eye className="h-4 w-4" />
                      <span>View</span>
                    </Link>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={onPageChange} />
      )}
    </div>
  );
}
