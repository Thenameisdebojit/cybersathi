import { MessageCircle, User, Bot, Clock } from 'lucide-react';

export default function ChatTranscript({ messages = [] }) {
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return new Intl.DateTimeFormat('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  if (!messages || messages.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-soft border border-gray-100 p-8 text-center">
        <div className="max-w-sm mx-auto">
          <div className="h-16 w-16 bg-gray-100 rounded-full mx-auto flex items-center justify-center mb-4">
            <MessageCircle className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Chat History</h3>
          <p className="text-gray-600 text-sm">
            No conversation transcript available for this complaint.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-soft border border-gray-100 overflow-hidden">
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 px-6 py-4 border-b border-primary-500">
        <div className="flex items-center gap-2 text-white">
          <MessageCircle className="h-5 w-5" />
          <h3 className="text-lg font-semibold">Chat Transcript</h3>
          <span className="ml-auto text-sm text-primary-100">{messages.length} messages</span>
        </div>
      </div>

      <div className="p-6 max-h-[600px] overflow-y-auto bg-gray-50">
        <div className="space-y-4">
          {messages.map((message, index) => {
            const isBot = message.sender === 'bot' || message.type === 'bot';
            const isUser = message.sender === 'user' || message.type === 'user';

            return (
              <div
                key={index}
                className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
              >
                <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center ${
                  isBot ? 'bg-primary-100' : 'bg-gray-200'
                }`}>
                  {isBot ? (
                    <Bot className="h-5 w-5 text-primary-700" />
                  ) : (
                    <User className="h-5 w-5 text-gray-700" />
                  )}
                </div>

                <div className={`flex-1 max-w-[75%] ${isUser ? 'flex justify-end' : ''}`}>
                  <div
                    className={`rounded-2xl px-4 py-3 ${
                      isBot
                        ? 'bg-white border border-gray-200'
                        : 'bg-primary-600 text-white'
                    }`}
                  >
                    <div className={`text-sm ${isBot ? 'text-gray-900' : 'text-white'}`}>
                      {message.text || message.content || message.message}
                    </div>
                    
                    <div className={`flex items-center gap-1 mt-2 text-xs ${
                      isBot ? 'text-gray-500' : 'text-primary-100'
                    }`}>
                      <Clock className="h-3 w-3" />
                      {formatTime(message.timestamp || message.created_at)}
                    </div>
                  </div>

                  {message.options && message.options.length > 0 && (
                    <div className="mt-2 space-y-2">
                      {message.options.map((option, idx) => (
                        <div
                          key={idx}
                          className="bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-700 hover:bg-gray-50"
                        >
                          {idx + 1}. {option}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="px-6 py-3 bg-gray-100 border-t border-gray-200">
        <p className="text-xs text-gray-600 text-center">
          All conversations are encrypted and stored securely in compliance with data protection regulations.
        </p>
      </div>
    </div>
  );
}
