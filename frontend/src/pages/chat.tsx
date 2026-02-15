import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../hooks/useAuth';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

const ChatPage: React.FC = () => {
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
    
    // Load previous conversation if available
    if (typeof window !== 'undefined') {
      const savedConversation = localStorage.getItem('currentChatConversation');
      if (savedConversation) {
        try {
          const parsed = JSON.parse(savedConversation);
          setMessages(parsed.messages);
          setCurrentConversationId(parsed.conversationId);
        } catch (e) {
          console.error('Error parsing saved conversation:', e);
        }
      }
    }
  }, []);

  // Save conversation to localStorage whenever messages change
  useEffect(() => {
    if (messages.length > 0) {
      const conversationData = {
        messages,
        conversationId: currentConversationId,
        timestamp: new Date().toISOString()
      };
      localStorage.setItem('currentChatConversation', JSON.stringify(conversationData));
    }
  }, [messages, currentConversationId]);

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
    localStorage.removeItem('currentChatConversation');
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-page">
      <div className="chat-container">
        <div className="chat-header">
          <div className="header-content">
            <h1>AI Assistant</h1>
            <p>Ask me anything about your tasks or just chat with me!</p>
          </div>
          <button onClick={startNewConversation} className="new-conversation-btn">
            New Chat
          </button>
        </div>

        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <div className="welcome-icon">🤖</div>
              <h2>Hello! I'm your AI assistant.</h2>
              <p>I can help you manage your tasks:</p>
              <ul>
                <li>Add tasks: "add task buy groceries"</li>
                <li>Show tasks: "show tasks"</li>
                <li>Delete tasks: "delete task 2"</li>
                <li>Update tasks: "update task 3 finish homework"</li>
              </ul>
              <p>Or just ask me anything!</p>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.role}`}
                >
                  <div className="message-content">
                    {message.content}
                  </div>
                  <div className="message-timestamp">
                    {formatTime(message.timestamp)}
                  </div>
                </div>
              ))}
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
            </>
          )}
        </div>

        <div className="input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
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

      <style jsx>{`
        .chat-page {
          display: flex;
          flex-direction: column;
          height: 100%;
          padding: 20px;
        }

        .chat-container {
          max-width: 800px;
          width: 100%;
          height: 100%;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          background: var(--card-bg);
          border-radius: var(--border-radius);
          border: 1px solid var(--card-border);
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .chat-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px;
          background: linear-gradient(135deg, var(--background-dark), var(--card-bg));
          border-bottom: 1px solid var(--card-border);
        }

        .header-content h1 {
          margin: 0;
          font-size: 24px;
          font-weight: 700;
          background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .header-content p {
          margin: 5px 0 0 0;
          color: var(--text-secondary);
          font-size: 14px;
        }

        .new-conversation-btn {
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: var(--border-radius);
          cursor: pointer;
          font-weight: 600;
          transition: all 0.2s ease;
        }

        .new-conversation-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        .messages-container {
          flex: 1;
          overflow-y: auto;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 15px;
          background: var(--background-darker);
        }

        .welcome-message {
          text-align: center;
          padding: 40px 20px;
          color: var(--text-secondary);
          flex: 1;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
        }

        .welcome-icon {
          font-size: 64px;
          margin-bottom: 20px;
        }

        .welcome-message h2 {
          margin: 0 0 15px 0;
          color: var(--text-primary);
          font-size: 24px;
        }

        .welcome-message p {
          margin: 0 0 10px 0;
          font-size: 16px;
        }

        .welcome-message ul {
          text-align: left;
          max-width: 500px;
          margin: 20px 0;
          padding-left: 20px;
        }

        .welcome-message li {
          margin-bottom: 8px;
          font-size: 15px;
          background: rgba(99, 102, 241, 0.1);
          padding: 8px 12px;
          border-radius: 8px;
        }

        .message {
          max-width: 85%;
          padding: 16px 20px;
          border-radius: 18px;
          position: relative;
          animation: fadeIn 0.3s ease;
          line-height: 1.5;
          word-wrap: break-word;
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
          font-size: 0.75rem;
          color: var(--text-muted);
          text-align: right;
          margin-top: 8px;
        }

        .input-container {
          display: flex;
          padding: 20px;
          background: var(--card-bg);
          border-top: 1px solid var(--card-border);
          gap: 12px;
        }

        textarea {
          flex: 1;
          padding: 14px 18px;
          background: rgba(30, 41, 59, 0.5);
          border: 1px solid var(--card-border);
          border-radius: var(--border-radius);
          resize: none;
          font-family: inherit;
          font-size: 15px;
          color: var(--text-primary);
          outline: none;
          transition: border-color 0.3s ease;
          min-height: 60px;
        }

        textarea:focus {
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        .send-button {
          padding: 14px 24px;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          color: white;
          border: none;
          border-radius: var(--border-radius);
          cursor: pointer;
          transition: all 0.3s ease;
          font-size: 15px;
          font-weight: 600;
          align-self: flex-end;
        }

        .send-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .send-button:not(:disabled):hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        @media (max-width: 768px) {
          .chat-container {
            height: calc(100vh - 140px);
            border-radius: 0;
          }

          .chat-header {
            flex-direction: column;
            gap: 15px;
            align-items: flex-start;
          }

          .header-content h1 {
            font-size: 20px;
          }

          .input-container {
            flex-direction: column;
          }

          .send-button {
            align-self: stretch;
          }

          .welcome-message ul {
            padding-left: 15px;
          }

          .welcome-message li {
            font-size: 14px;
            padding: 6px 10px;
          }
        }

        @media (max-width: 480px) {
          .chat-container {
            height: calc(100vh - 120px);
          }

          .chat-header {
            padding: 15px;
          }

          .header-content h1 {
            font-size: 18px;
          }

          .header-content p {
            font-size: 13px;
          }

          .new-conversation-btn {
            padding: 8px 16px;
            font-size: 0.9rem;
          }

          .messages-container {
            padding: 15px 10px;
          }

          .welcome-message {
            padding: 20px 10px;
          }

          .welcome-icon {
            font-size: 48px;
          }

          .welcome-message h2 {
            font-size: 20px;
          }

          .welcome-message p {
            font-size: 14px;
          }

          .input-container {
            padding: 15px 10px;
          }

          textarea {
            padding: 12px 16px;
            font-size: 14px;
            min-height: 50px;
          }

          .send-button {
            padding: 12px;
            font-size: 0.9rem;
          }
        }
      `}</style>
    </div>
  );
};

export default ChatPage;