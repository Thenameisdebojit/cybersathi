import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Shield, Mail, Lock, Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-react';
import { authService } from '../services/auth';
import Loader from '../components/ui/Loader';
import Logo from '../components/Logo';

export default function NewLoginPage() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await authService.login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-700 via-primary-600 to-primary-800 p-12 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10" />
        
        <div className="relative z-10 flex flex-col justify-between w-full">
          <div className="flex items-center gap-3">
            <div className="h-14 w-14 bg-white bg-opacity-20 backdrop-blur-sm rounded-2xl flex items-center justify-center shadow-large">
              <Shield className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">CyberSathi</h1>
              <p className="text-primary-100 text-sm font-medium">Admin Console</p>
            </div>
          </div>

          <div className="space-y-8">
            <div>
              <h2 className="text-4xl font-bold mb-4">Secure Cybercrime Management System</h2>
              <p className="text-lg text-primary-100 leading-relaxed">
                Empowering law enforcement and government agencies to efficiently manage and resolve cybercrime complaints through our comprehensive admin dashboard.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-6">
              {[
                { icon: Shield, title: 'Secure & Compliant', desc: 'Bank-grade security with data encryption' },
                { icon: CheckCircle, title: 'Real-time Tracking', desc: 'Monitor complaint status instantly' },
                { icon: AlertCircle, title: 'Smart Analytics', desc: 'AI-powered insights and reporting' },
                { icon: Mail, title: 'Multi-channel Support', desc: 'WhatsApp, Web, and API integration' },
              ].map(({ icon: Icon, title, desc }, idx) => (
                <div key={idx} className="bg-white bg-opacity-10 backdrop-blur-sm rounded-xl p-4 border border-white border-opacity-20">
                  <Icon className="h-8 w-8 mb-2 text-primary-100" />
                  <h3 className="font-semibold mb-1">{title}</h3>
                  <p className="text-sm text-primary-100">{desc}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="text-sm text-primary-100">
            <p>© 2024 CyberSathi. Ministry of Home Affairs, Government of India.</p>
            <p className="mt-1">National Cybercrime Helpline: <span className="font-bold text-white">1930</span></p>
          </div>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-8 bg-gray-50">
        <div className="w-full max-w-md">
          <div className="lg:hidden text-center mb-8">
            <div className="inline-flex h-16 w-16 bg-primary-600 rounded-2xl items-center justify-center shadow-medium mb-4">
              <Shield className="h-9 w-9 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">CyberSathi Admin</h1>
            <p className="text-gray-600 mt-1">Sign in to access your dashboard</p>
          </div>

          <div className="bg-white rounded-2xl shadow-large p-8 border border-gray-100">
            <div className="hidden lg:block mb-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">Welcome back</h2>
              <p className="text-gray-600">Sign in to access your dashboard</p>
            </div>

            {error && (
              <div className="mb-6 p-4 bg-danger-50 border border-danger-200 rounded-xl flex items-start gap-3 animate-slide-up">
                <AlertCircle className="h-5 w-5 text-danger-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-danger-900">Authentication Error</h4>
                  <p className="text-sm text-danger-700 mt-1">{error}</p>
                </div>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    id="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-gray-900 placeholder-gray-400"
                    placeholder="admin@cybersathi.in"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    id="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all text-gray-900 placeholder-gray-400"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                  />
                  <span className="ml-2 text-sm text-gray-600">Remember me</span>
                </label>
                <a href="#" className="text-sm font-medium text-primary-600 hover:text-primary-700">
                  Forgot password?
                </a>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-xl shadow-medium hover:shadow-large transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader size="sm" />
                    <span>Signing in...</span>
                  </>
                ) : (
                  <span>Sign In</span>
                )}
              </button>
            </form>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <p className="text-center text-sm text-gray-600">
                Don't have an account?{' '}
                <Link to="/signup" className="font-medium text-primary-600 hover:text-primary-700">
                  Sign up here
                </Link>
              </p>
              <p className="text-center text-sm text-gray-600 mt-2">
                Having trouble signing in?{' '}
                <a href="#" className="font-medium text-primary-600 hover:text-primary-700">
                  Contact Support
                </a>
              </p>
            </div>

            <div className="mt-6 p-4 bg-primary-50 rounded-xl border border-primary-100">
              <p className="text-xs text-primary-900 font-medium mb-2">Default Credentials (Development)</p>
              <code className="text-xs text-primary-700 block">Email: admin@cybersathi.in</code>
              <code className="text-xs text-primary-700 block mt-1">Password: Check .env file</code>
            </div>
          </div>

          <p className="mt-6 text-center text-xs text-gray-500">
            Protected by enterprise-grade security. All access is monitored and logged.
          </p>
        </div>
      </div>
    </div>
  );
}
