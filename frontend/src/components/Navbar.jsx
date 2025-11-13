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
    <nav className="bg-white shadow-soft border-b border-gray-100 sticky top-0 z-50 backdrop-blur-sm bg-white/95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="h-10 w-10 bg-gradient-primary rounded-xl flex items-center justify-center shadow-medium">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <span className="ml-3 text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-700 to-success-700">CyberSathi</span>
            <span className="ml-3 text-sm text-gray-500 hidden lg:inline font-medium">Cybercrime Helpline 1930</span>
          </div>
          
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all duration-200 min-h-touch ${
                  isActive(path) 
                    ? 'bg-primary-50 text-primary-700 shadow-sm' 
                    : 'text-gray-700 hover:bg-gray-50 hover:text-primary-600'
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
