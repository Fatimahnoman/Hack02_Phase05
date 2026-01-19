import React from 'react';
import Layout from '../components/layout/Layout';
import ChatInterface from '../components/chat/ChatInterface';
import { useAuth } from '../hooks/useAuth';

const ChatPage = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Layout>
      <div className="chat-page">
        {!isAuthenticated ? (
          <div className="auth-prompt">
            <h2>Please sign in to use the chat</h2>
            <p>You need to be signed in to access the chat interface.</p>
          </div>
        ) : (
          <ChatInterface />
        )}
      </div>
      <style jsx global>{`
        .chat-page {
          padding: 20px;
          max-width: 1200px;
          margin: 0 auto;
          width: 100%;
        }

        .auth-prompt {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          padding: 40px 20px;
          color: #4a5568;
        }

        .auth-prompt h2 {
          margin-bottom: 15px;
          color: #2d3748;
        }
      `}</style>
    </Layout>
  );
};

export default ChatPage;