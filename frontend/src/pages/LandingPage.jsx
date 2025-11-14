import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, ArrowRight, Lock, TrendingUp, MessageCircle, Globe, CheckCircle, Zap } from 'lucide-react';
import Logo from '../components/Logo';

export default function LandingPage() {
  const navigate = useNavigate();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setTimeout(() => setIsVisible(true), 100);
  }, []);

  const features = [
    {
      icon: Shield,
      title: 'Secure & Compliant',
      description: 'Bank-grade security with data encryption and compliance with government standards'
    },
    {
      icon: TrendingUp,
      title: 'Real-time Analytics',
      description: 'Monitor cybercrime trends and complaint resolution with powerful analytics'
    },
    {
      icon: MessageCircle,
      title: 'Multi-channel Support',
      description: 'WhatsApp, Web, and API integration for seamless complaint management'
    },
    {
      icon: Globe,
      title: 'National Network',
      description: 'Connected to India\'s National Cybercrime Helpline 1930'
    }
  ];

  const stats = [
    { value: '10,000+', label: 'Complaints Resolved' },
    { value: '₹50Cr+', label: 'Funds Recovered' },
    { value: '24/7', label: 'Support Available' },
    { value: '500+', label: 'Law Enforcement Agencies' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Navigation Bar */}
      <nav className="relative z-10 container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Logo size="large" />
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/login')}
              className="text-white hover:text-blue-200 font-medium transition-colors"
            >
              Sign In
            </button>
            <button
              onClick={() => navigate('/signup')}
              className="bg-white text-blue-900 px-6 py-2.5 rounded-lg font-semibold hover:bg-blue-50 transition-all shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className={`relative z-10 container mx-auto px-6 pt-12 pb-20 transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
        <div className="max-w-6xl mx-auto">
          {/* Main Hero */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 bg-blue-500/20 backdrop-blur-sm text-white px-4 py-2 rounded-full mb-6 border border-blue-400/30">
              <Zap className="h-4 w-4 text-yellow-300" />
              <span className="text-sm font-medium">India's Premier Cybercrime Management System</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
              Protect Citizens.<br />
              <span className="bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                Fight Cybercrime.
              </span>
            </h1>
            
            <p className="text-xl text-blue-100 mb-10 max-w-3xl mx-auto leading-relaxed">
              Empowering law enforcement and government agencies to efficiently manage, track, and resolve cybercrime complaints through our comprehensive admin dashboard.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button
                onClick={() => navigate('/login')}
                className="group bg-white text-blue-900 px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-50 transition-all shadow-2xl hover:shadow-blue-500/50 transform hover:scale-105 flex items-center gap-2"
              >
                Access Dashboard
                <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button
                onClick={() => window.location.href = 'tel:1930'}
                className="border-2 border-white text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-white/10 transition-all backdrop-blur-sm"
              >
                Call 1930 Helpline
              </button>
            </div>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20">
            {stats.map((stat, index) => (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-md rounded-2xl p-6 text-center border border-white/20 hover:bg-white/15 transition-all transform hover:scale-105"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="text-3xl md:text-4xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-blue-200 text-sm font-medium">{stat.label}</div>
              </div>
            ))}
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 gap-6 mb-16">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all transform hover:scale-105 hover:shadow-2xl"
                  style={{ animationDelay: `${index * 150}ms` }}
                >
                  <div className="bg-blue-500/30 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
                    <Icon className="h-7 w-7 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                  <p className="text-blue-100 leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </div>

          {/* Key Features */}
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <h3 className="text-2xl font-bold text-white mb-6 text-center">Complete PS-2 Compliance</h3>
            <div className="grid md:grid-cols-2 gap-4">
              {[
                'Complaint Registration & Tracking',
                'Account Unfreeze Requests',
                'Evidence Management System',
                '23 Financial Fraud Categories',
                'Social Media Fraud Tracking',
                'Real-time Analytics Dashboard',
                'WhatsApp Integration',
                'AI-Powered Chatbot Support'
              ].map((feature, index) => (
                <div key={index} className="flex items-center gap-3">
                  <CheckCircle className="h-5 w-5 text-green-400 flex-shrink-0" />
                  <span className="text-blue-100">{feature}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="relative z-10 border-t border-white/10 bg-black/20 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="text-blue-200 text-sm mb-4 md:mb-0">
              © 2024 CyberSathi. Ministry of Home Affairs, Government of India.
            </div>
            <div className="text-blue-200 text-sm">
              National Cybercrime Helpline: <span className="font-bold text-white">1930</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
