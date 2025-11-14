export default function StatusBadge({ status }) {
  const getStatusConfig = (status) => {
    const configs = {
      registered: {
        bg: 'bg-primary-100',
        text: 'text-primary-800',
        label: 'New',
      },
      under_review: {
        bg: 'bg-warning-100',
        text: 'text-warning-800',
        label: 'In Progress',
      },
      resolved: {
        bg: 'bg-success-100',
        text: 'text-success-800',
        label: 'Resolved',
      },
      closed: {
        bg: 'bg-gray-100',
        text: 'text-gray-800',
        label: 'Closed',
      },
      escalated: {
        bg: 'bg-danger-100',
        text: 'text-danger-800',
        label: 'Escalated',
      },
    };

    return configs[status] || configs.registered;
  };

  const config = getStatusConfig(status);

  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${config.bg} ${config.text}`}
    >
      <span className={`h-2 w-2 rounded-full ${config.text.replace('text-', 'bg-')} mr-2`} />
      {config.label}
    </span>
  );
}
