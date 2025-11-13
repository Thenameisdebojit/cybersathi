import { Link, useLocation } from 'react-router-dom';
import { Shield, LayoutDashboard, FileText, BarChart2, Megaphone, Menu } from 'lucide-react';
import UserProfileDropdown from './UserProfileDropdown';

export default function Navbar() {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/complaints', label: 'Complaints', icon: FileText },
    { path: '/analytics', label: 'Analytics', icon: BarChart2 },
    { path: '/campaigns', label: 'Campaigns', icon: Megaphone },
  ];
  
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-indigo-600" />
            <span className="ml-2 text-xl font-bold text-gray-900">CyberSathi</span>
            <span className="ml-2 text-sm text-gray-500 hidden lg:inline">Cybercrime Helpline 1930</span>
          </div>
          
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 transition ${
                  isActive(path) 
                    ? 'bg-indigo-50 text-indigo-600' 
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            ))}
          </div>

          <div className="flex items-center">
            <UserProfileDropdown />
          </div>
        </div>
      </div>
    </nav>
  );
}
