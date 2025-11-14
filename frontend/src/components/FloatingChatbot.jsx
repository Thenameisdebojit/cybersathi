import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, Loader2 } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function FloatingChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your CyberSathi AI assistant. I can help you with questions about cybercrime, fraud prevention, and how to report incidents. How can I assist you today?'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');

    const newMessages = [...messages, { role: 'user', content: userMessage }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/ai/chat`, {
        messages: newMessages.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        max_tokens: 500
      });

      setMessages([
        ...newMessages,
        { role: 'assistant', content: response.data.message }
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      let errorMessage = 'I apologize, but I encountered an error. Please try again or call the 1930 helpline for immediate assistance.';
      
      if (error.response?.status === 503) {
        errorMessage = '⚠️ The AI chatbot is currently not configured. Please contact the administrator to set up the OpenAI API key, or call the 1930 helpline for immediate assistance.';
      } else if (error.response?.data?.detail) {
        errorMessage = `Error: ${error.response.data.detail}. Please call the 1930 helpline for immediate assistance.`;
      }
      
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: errorMessage
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const exampleQuestions = [
    'What is UPI fraud?',
    'How to file a complaint?',
    'What is digital arrest fraud?',
    'My account was hacked'
  ];

  const handleExampleClick = (question) => {
    setInputMessage(question);
  };

  return (
    <>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-full p-4 shadow-lg hover:shadow-xl transition-all hover:scale-110 z-50 flex items-center gap-2 group"
          aria-label="Open AI Chatbot"
        >
          <MessageCircle className="h-6 w-6" />
          <span className="hidden group-hover:inline-block text-sm font-medium pr-2">
            Ask me about cybercrime
          </span>
        </button>
      )}

      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[600px] bg-white rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden border border-gray-200">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-white/20 rounded-full p-2">
                <MessageCircle className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-semibold">CyberSathi AI</h3>
                <p className="text-xs text-blue-100">Ask about cybercrime</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="hover:bg-white/20 rounded-full p-1 transition-colors"
              aria-label="Close chatbot"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-white text-gray-800 rounded-bl-none shadow-sm border border-gray-200'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-800 rounded-2xl rounded-bl-none px-4 py-2 shadow-sm border border-gray-200">
                  <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                </div>
              </div>
            )}

            {messages.length === 1 && (
              <div className="space-y-2">
                <p className="text-xs text-gray-500 font-medium">Quick questions:</p>
                {exampleQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleExampleClick(question)}
                    className="block w-full text-left text-sm bg-white hover:bg-blue-50 border border-gray-200 rounded-lg px-3 py-2 transition-colors"
                  >
                    {question}
                  </button>
                ))}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="p-4 bg-white border-t border-gray-200">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about cybercrime..."
                className="flex-1 border border-gray-300 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isLoading}
                className="bg-blue-600 text-white rounded-full p-2 hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label="Send message"
              >
                <Send className="h-5 w-5" />
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Powered by AI • Call 1930 for emergencies
            </p>
          </div>
        </div>
      )}
    </>
  );
}
