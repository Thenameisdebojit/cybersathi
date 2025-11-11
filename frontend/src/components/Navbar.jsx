import { Link, useLocation } from 'react-router-dom';
import { Shield, LayoutDashboard, Search, BookOpen, Menu } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-primary-600" />
            <span className="ml-2 text-xl font-bold text-gray-900">CyberSathi</span>
            <span className="ml-2 text-sm text-gray-500">Cybercrime Helpline 1930</span>
          </div>
          
          <div className="hidden md:flex items-center space-x-1">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 ${
                isActive('/') ? 'bg-primary-50 text-primary-600' : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <LayoutDashboard className="h-4 w-4" />
              Dashboard
            </Link>
            <Link
              to="/tracker"
              className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 ${
                isActive('/tracker') ? 'bg-primary-50 text-primary-600' : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Search className="h-4 w-4" />
              Case Tracker
            </Link>
            <Link
              to="/awareness"
              className={`px-3 py-2 rounded-md text-sm font-medium flex items-center gap-2 ${
                isActive('/awareness') ? 'bg-primary-50 text-primary-600' : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <BookOpen className="h-4 w-4" />
              Awareness Center
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
