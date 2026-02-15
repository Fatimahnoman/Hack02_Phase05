import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../hooks/useAuth';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const FloatingChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const { user, isAuthenticated } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading || !isAuthenticated) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      role: 'user',
      timestamp: new Date(),
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      // Call the backend chat API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({
          user_input: messageToSend,
          user_id: user ? user.id.toString() : 'anonymous',
          session_metadata: {
            conversation_id: currentConversationId || undefined
          }
        }),
      });

      if (!response.ok) {
        throw new Error(`Chat API error: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if this is the first message
      if (!currentConversationId) {
        setCurrentConversationId(data.conversation_id);
      }

      const assistantMessage: Message = {
        id: Date.now().toString(),
        content: data.response,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setCurrentConversationId(null);
  };

  return (
    <div className="floating-chat-widget">
      {/* Floating Button */}
      <button
        className={`chat-toggle-btn ${isOpen ? 'open' : ''}`}
        onClick={() => {
          if (isAuthenticated) {
            setIsOpen(!isOpen);
          } else {
            alert('Please sign in to use the chat');
          }
        }}
      >
        {isOpen ? '×' : '💬'}
      </button>

      {/* Chat Popup */}
      {isOpen && isAuthenticated && (
        <div className="chat-popup">
          <div className="chat-header">
            <h3>AI Assistant</h3>
            <button onClick={startNewConversation} className="new-conversation-btn">
              New Chat
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="close-btn"
            >
              ×
            </button>
          </div>

          <div className="messages-container">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <h4>Hello! I'm your AI assistant.</h4>
                <p>Ask me anything about your todos, or just chat with me!</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.role}`}
                >
                  <div className="message-content">
                    {message.content}
                  </div>
                  <div className="message-timestamp">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-container">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isLoading}
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="send-button"
            >
              Send
            </button>
          </div>
        </div>
      )}

      {/* Auth Prompt when not authenticated */}
      {isOpen && !isAuthenticated && (
        <div className="chat-popup">
          <div className="chat-header">
            <h3>AI Assistant</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="close-btn"
            >
              ×
            </button>
          </div>
          <div className="auth-prompt">
            <p>Please sign in to use the chat assistant.</p>
          </div>
        </div>
      )}

      <style jsx>{`
        .floating-chat-widget {
          position: fixed;
          bottom: 20px;
          right: 20px;
          z-index: 1000;
        }

        .chat-toggle-btn {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          border: none;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          font-size: 24px;
          cursor: pointer;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
        }

        .chat-toggle-btn::before {
          content: '';
          position: absolute;
          top: -2px;
          left: -2px;
          right: -2px;
          bottom: -2px;
          background: linear-gradient(45deg, var(--primary-color), var(--accent-color), var(--secondary-color));
          border-radius: 50%;
          z-index: -1;
          opacity: 0;
          transition: opacity 0.3s ease;
        }

        .chat-toggle-btn:hover {
          transform: scale(1.1);
          box-shadow: 0 6px 25px rgba(99, 102, 241, 0.4);
        }

        .chat-toggle-btn:hover::before {
          opacity: 1;
        }

        .chat-toggle-btn.open {
          background: linear-gradient(135deg, var(--danger), #dc2626);
        }

        .chat-popup {
          position: absolute;
          bottom: 80px;
          right: 0;
          width: 380px;
          height: 550px;
          background: var(--card-bg);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          animation: slideUp 0.3s ease;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .chat-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 18px 20px;
          background: linear-gradient(135deg, var(--card-bg), var(--background-dark));
          border-bottom: 1px solid var(--card-border);
          color: var(--text-primary);
        }

        .chat-header h3 {
          margin: 0;
          font-size: 1.2rem;
          font-weight: 600;
          background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .new-conversation-btn {
          background: rgba(99, 102, 241, 0.15);
          color: var(--primary-color);
          border: 1px solid rgba(99, 102, 241, 0.3);
          padding: 6px 12px;
          border-radius: var(--border-radius);
          cursor: pointer;
          font-size: 0.8rem;
          font-weight: 500;
          transition: all 0.2s ease;
        }

        .new-conversation-btn:hover {
          background: rgba(99, 102, 241, 0.25);
          transform: translateY(-2px);
        }

        .close-btn {
          background: none;
          border: none;
          color: var(--text-secondary);
          font-size: 24px;
          cursor: pointer;
          padding: 0;
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: all 0.2s ease;
        }

        .close-btn:hover {
          background: rgba(255, 255, 255, 0.1);
          color: var(--text-primary);
        }

        .messages-container {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 15px;
          background: var(--background-dark);
        }

        .welcome-message {
          text-align: center;
          padding: 20px;
          color: var(--text-secondary);
        }

        .welcome-message h4 {
          margin: 0 0 10px 0;
          color: var(--text-primary);
          font-weight: 600;
        }

        .message {
          max-width: 85%;
          padding: 14px 18px;
          border-radius: 18px;
          position: relative;
          animation: fadeIn 0.3s ease;
          line-height: 1.5;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .user {
          align-self: flex-end;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          border-bottom-right-radius: 5px;
        }

        .assistant {
          align-self: flex-start;
          background: var(--card-bg);
          color: var(--text-primary);
          border: 1px solid var(--card-border);
          border-bottom-left-radius: 5px;
        }

        .message-content {
          word-wrap: break-word;
        }

        .typing-indicator {
          display: flex;
          gap: 5px;
          padding: 5px 0;
        }

        .typing-indicator span {
          width: 8px;
          height: 8px;
          background: var(--text-secondary);
          border-radius: 50%;
          animation: bounce 1.5s infinite ease-in-out;
        }

        .typing-indicator span:nth-child(2) {
          animation-delay: 0.2s;
        }

        .typing-indicator span:nth-child(3) {
          animation-delay: 0.4s;
        }

        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-5px); }
        }

        .message-timestamp {
          font-size: 0.7rem;
          color: var(--text-muted);
          text-align: right;
          margin-top: 5px;
        }

        .input-container {
          display: flex;
          padding: 15px;
          background: var(--card-bg);
          border-top: 1px solid var(--card-border);
        }

        textarea {
          flex: 1;
          padding: 12px 16px;
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          resize: none;
          font-family: inherit;
          font-size: 0.9rem;
          color: var(--text-primary);
          outline: none;
          transition: border-color 0.3s ease;
        }

        textarea:focus {
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .send-button {
          margin-left: 10px;
          padding: 12px 20px;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          border: none;
          border-radius: var(--border-radius);
          cursor: pointer;
          transition: all 0.3s ease;
          font-size: 0.9rem;
          font-weight: 600;
        }

        .send-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .send-button:not(:disabled):hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        .auth-prompt {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
          text-align: center;
          color: var(--text-secondary);
        }

        @media (max-width: 768px) {
          .chat-popup {
            width: 320px;
            height: 450px;
            right: 0;
          }

          .chat-toggle-btn {
            width: 55px;
            height: 55px;
          }
        }

        @media (max-width: 480px) {
          .chat-popup {
            width: calc(100vw - 20px);
            height: 400px;
            bottom: 70px;
            right: 10px;
            left: 10px;
          }

          .chat-header {
            padding: 15px;
          }

          .chat-header h3 {
            font-size: 1.1rem;
          }

          .new-conversation-btn {
            padding: 5px 10px;
            font-size: 0.75rem;
          }

          .messages-container {
            padding: 15px;
          }

          .message {
            max-width: 90%;
            padding: 12px 16px;
          }

          .input-container {
            padding: 12px;
          }

          textarea {
            padding: 10px 14px;
            font-size: 0.85rem;
          }

          .send-button {
            padding: 10px 16px;
            font-size: 0.85rem;
          }
        }
      `}</style>
    </div>
  );
};

export default FloatingChatWidget;