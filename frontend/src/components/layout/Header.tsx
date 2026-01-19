import React from 'react';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';

const Header = () => {
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          {isAuthenticated && (
            <nav className="nav">
              <Link href="/dashboard">Dashboard</Link>
              <Link href="/chat">Chat</Link>
              <span>Welcome, {user?.email}</span>
              <button onClick={handleLogout}>Logout</button>
            </nav>
          )}
        </div>
      </div>
      <style jsx>{`
        .header {
          background: linear-gradient(135deg, #000000 0%, #333333 100%);
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
          padding: 15px 0;
          position: sticky;
          top: 0;
          z-index: 1000;
          backdrop-filter: blur(10px);
        }

        .header-content {
          display: flex;
          justify-content: flex-end;
          align-items: center;
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 20px;
        }

        .nav {
          display: flex;
          align-items: center;
          gap: 25px;
        }

        .nav a,
        .nav button,
        .nav span {
          text-decoration: none;
          color: white;
          padding: 10px 16px;
          border-radius: 8px;
          background: rgba(255, 255, 255, 0.2);
          border: none;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 500;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .nav a:hover,
        .nav button:hover {
          background: rgba(255, 255, 255, 0.3);
          transform: translateY(-2px);
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }

        .nav span {
          background: rgba(255, 255, 255, 0.1);
          font-weight: 600;
        }

        @media (max-width: 768px) {
          .header-content {
            flex-direction: column;
            gap: 15px;
            padding: 0 15px;
          }

          .nav {
            width: 100%;
            justify-content: center;
            flex-wrap: wrap;
            gap: 12px;
          }

          .nav a,
          .nav button,
          .nav span {
            padding: 8px 12px;
            font-size: 0.9rem;
          }
        }
      `}</style>
    </header>
  );
};

export default Header;