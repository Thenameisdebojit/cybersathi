import { Shield, AlertTriangle, Lock, Mail, CreditCard, Smartphone, CheckCircle } from 'lucide-react';

export default function AwarenessPage() {
  const tips = [
    {
      icon: Lock,
      title: 'Never Share OTP or PIN',
      description: 'No legitimate organization will ask for your OTP, CVV, or PIN. Keep these completely confidential.',
      color: 'bg-red-500'
    },
    {
      icon: Mail,
      title: 'Beware of Phishing',
      description: 'Be cautious of emails or messages asking for personal information. Verify the sender before clicking links.',
      color: 'bg-orange-500'
    },
    {
      icon: CreditCard,
      title: 'Secure Online Payments',
      description: 'Only use secure payment gateways. Look for HTTPS and padlock icon in the browser address bar.',
      color: 'bg-blue-500'
    },
    {
      icon: Smartphone,
      title: 'Enable Two-Factor Authentication',
      description: 'Add an extra layer of security to your accounts with 2FA. Use authenticator apps when possible.',
      color: 'bg-green-500'
    },
    {
      icon: AlertTriangle,
      title: 'Verify Before Trusting',
      description: 'If an offer seems too good to be true, it probably is. Verify independently before taking action.',
      color: 'bg-yellow-500'
    },
    {
      icon: Shield,
      title: 'Keep Software Updated',
      description: 'Regularly update your operating system, apps, and antivirus software to patch security vulnerabilities.',
      color: 'bg-purple-500'
    }
  ];

  const commonScams = [
    {
      title: 'UPI Frauds',
      description: 'Fraudsters send fake payment requests or ask you to share QR codes to steal money.',
      prevention: 'Always verify the recipient before making payments. Never share QR codes or payment links.'
    },
    {
      title: 'Job Scams',
      description: 'Fake job offers asking for upfront fees or personal documents.',
      prevention: 'Legitimate employers never ask for payment. Research the company thoroughly before applying.'
    },
    {
      title: 'Online Shopping Fraud',
      description: 'Fake websites selling products at very low prices but never delivering.',
      prevention: 'Use trusted e-commerce platforms. Check reviews and seller ratings before purchasing.'
    },
    {
      title: 'Investment Scams',
      description: 'Promises of guaranteed high returns with minimal risk.',
      prevention: 'Consult financial experts. Remember: high returns always come with high risk.'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Cyber Safety Awareness</h1>
        <p className="text-gray-600 mt-1">Stay safe online with these essential cybersecurity tips</p>
      </div>

      <div className="mb-12 bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-8 text-white">
        <div className="flex items-center gap-3 mb-4">
          <Shield className="h-10 w-10" />
          <h2 className="text-2xl font-bold">National Cybercrime Helpline</h2>
        </div>
        <p className="text-lg mb-4">For immediate assistance or to report cybercrime</p>
        <div className="flex items-center gap-6">
          <div>
            <p className="text-sm opacity-90">Call Now</p>
            <p className="text-3xl font-bold">1930</p>
          </div>
          <div className="h-12 w-px bg-white opacity-30"></div>
          <div>
            <p className="text-sm opacity-90">Report Online</p>
            <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" 
               className="text-lg font-semibold underline hover:opacity-80">
              cybercrime.gov.in
            </a>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Essential Cyber Safety Tips</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tips.map((tip, index) => (
            <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className={`inline-flex p-3 rounded-lg ${tip.color} mb-4`}>
                <tip.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{tip.title}</h3>
              <p className="text-sm text-gray-600">{tip.description}</p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Common Scams to Watch Out For</h2>
        <div className="space-y-4">
          {commonScams.map((scam, index) => (
            <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{scam.title}</h3>
              <p className="text-sm text-gray-600 mb-3">{scam.description}</p>
              <div className="flex items-start gap-2 p-3 bg-green-50 rounded-lg">
                <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-xs font-medium text-green-900 mb-1">How to Prevent</p>
                  <p className="text-sm text-green-800">{scam.prevention}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
