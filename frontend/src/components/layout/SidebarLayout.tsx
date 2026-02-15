import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';
import FloatingChatWidget from '../chat/FloatingChatWidget';

interface SidebarLayoutProps {
  children: React.ReactNode;
  title?: string;
}

const SidebarLayout: React.FC<SidebarLayoutProps> = ({ children, title }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
      if (window.innerWidth < 768) {
        setSidebarOpen(false);
      } else {
        setSidebarOpen(true);
      }
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);

    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const menuItems = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Tasks', href: '/tasks', icon: '✅' },
    { name: 'Chatbot', href: '/chat', icon: '🤖' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
  ];

  return (
    <>
      <Head>
        <title>{title ? `${title} - Evolution of Todo` : 'Evolution of Todo'}</title>
        <meta name="description" content="A modern todo application" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="app-container">
        {/* Sidebar */}
        <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <div className="sidebar-header">
            <Link href="/dashboard" legacyBehavior>
              <a>
                <div className="logo">
                  <div className="logo-icon">📋</div>
                  <h1 className="logo-text">Evolution</h1>
                </div>
              </a>
            </Link>
            
            {isMobile && (
              <button className="close-sidebar-btn" onClick={toggleSidebar}>
                ✕
              </button>
            )}
          </div>
          
          <nav className="sidebar-nav">
            <ul>
              {menuItems.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} legacyBehavior>
                    <a className="nav-link">
                      <span className="nav-icon">{item.icon}</span>
                      <span className="nav-text">{item.name}</span>
                    </a>
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          {/* Top Navbar */}
          <header className="top-navbar">
            <button className="sidebar-toggle-btn" onClick={toggleSidebar}>
              ☰
            </button>
            
            <div className="navbar-content">
              <h2>{title || 'Dashboard'}</h2>
              
              <div className="user-section">
                <div className="user-info">
                  <span className="user-name">{user?.email || 'User'}</span>
                  <div className="user-avatar">👤</div>
                </div>
              </div>
            </div>
          </header>
          
          {/* Page Content */}
          <div className="page-content">
            {children}
          </div>
        </main>
        
        {/* Floating Chat Widget */}
        <FloatingChatWidget />
      </div>

      <style jsx global>{`
        :root {
          --sidebar-width: 260px;
          --sidebar-collapsed-width: 70px;
          --navbar-height: 70px;
          --primary-color: #6366f1;
          --primary-dark: #4f46e5;
          --secondary-color: #8b5cf6;
          --accent-color: #ec4899;
          --background-dark: #0f172a;
          --background-darker: #020617;
          --card-bg: #111827;
          --card-border: #1f2937;
          --text-primary: #f8fafc;
          --text-secondary: #cbd5e1;
          --text-muted: #94a3b8;
          --success: #10b981;
          --warning: #f59e0b;
          --danger: #ef4444;
          --border-radius: 12px;
          --transition-speed: 0.3s;
        }

        body {
          margin: 0;
          padding: 0;
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
            Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
          background-color: var(--background-darker);
          color: var(--text-primary);
          overflow-x: hidden;
        }

        .app-container {
          display: flex;
          min-height: 100vh;
        }

        /* Sidebar Styles */
        .sidebar {
          width: var(--sidebar-width);
          background: linear-gradient(160deg, var(--background-dark) 0%, var(--background-darker) 100%);
          color: var(--text-primary);
          height: 100vh;
          position: fixed;
          top: 0;
          left: 0;
          z-index: 100;
          transition: all var(--transition-speed) ease;
          border-right: 1px solid var(--card-border);
          display: flex;
          flex-direction: column;
          box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
        }

        .sidebar.closed {
          transform: translateX(calc(var(--sidebar-width) * -1));
          width: var(--sidebar-collapsed-width);
        }

        .sidebar-header {
          padding: 24px 20px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 1px solid var(--card-border);
        }

        .logo {
          display: flex;
          align-items: center;
          gap: 12px;
          cursor: pointer;
        }

        .logo-icon {
          font-size: 28px;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          border-radius: 10px;
        }

        .logo-text {
          font-size: 22px;
          font-weight: 700;
          background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin: 0;
        }

        .close-sidebar-btn {
          background: none;
          border: none;
          color: var(--text-primary);
          font-size: 24px;
          cursor: pointer;
          padding: 8px;
          border-radius: 50%;
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .close-sidebar-btn:hover {
          background: rgba(255, 255, 255, 0.1);
        }

        .sidebar-nav {
          flex: 1;
          padding: 20px 0;
          overflow-y: auto;
        }

        .sidebar-nav ul {
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .sidebar-nav li {
          margin-bottom: 4px;
        }

        .nav-link {
          display: flex;
          align-items: center;
          padding: 14px 20px;
          color: var(--text-secondary);
          text-decoration: none;
          transition: all 0.2s ease;
          border-left: 3px solid transparent;
        }

        .nav-link:hover {
          background: rgba(255, 255, 255, 0.05);
          color: var(--text-primary);
        }

        .nav-link.active {
          background: rgba(99, 102, 241, 0.15);
          color: var(--primary-color);
          border-left: 3px solid var(--primary-color);
        }

        .nav-icon {
          font-size: 20px;
          margin-right: 12px;
          width: 24px;
          text-align: center;
        }

        .nav-text {
          font-size: 16px;
          font-weight: 500;
        }

        /* Main Content Styles */
        .main-content {
          flex: 1;
          display: flex;
          flex-direction: column;
          margin-left: var(--sidebar-width);
          transition: margin-left var(--transition-speed) ease;
        }

        .sidebar.closed + .main-content {
          margin-left: var(--sidebar-collapsed-width);
        }

        /* Top Navbar Styles */
        .top-navbar {
          height: var(--navbar-height);
          background: linear-gradient(160deg, var(--card-bg) 0%, var(--background-dark) 100%);
          border-bottom: 1px solid var(--card-border);
          display: flex;
          align-items: center;
          padding: 0 24px;
          position: sticky;
          top: 0;
          z-index: 90;
        }

        .sidebar-toggle-btn {
          background: none;
          border: none;
          color: var(--text-primary);
          font-size: 24px;
          cursor: pointer;
          padding: 8px;
          border-radius: 8px;
          margin-right: 16px;
          display: none;
        }

        @media (max-width: 768px) {
          .sidebar-toggle-btn {
            display: block;
          }
        }

        .navbar-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          width: 100%;
        }

        .navbar-content h2 {
          margin: 0;
          font-size: 20px;
          font-weight: 600;
          color: var(--text-primary);
        }

        .user-section {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .user-info {
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .user-name {
          font-weight: 500;
          color: var(--text-primary);
          font-size: 15px;
        }

        .user-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 20px;
        }

        /* Page Content Styles */
        .page-content {
          flex: 1;
          padding: 30px;
          background: linear-gradient(160deg, var(--background-dark) 0%, var(--background-darker) 100%);
          min-height: calc(100vh - var(--navbar-height));
        }

        /* Responsive adjustments */
        @media (max-width: 1024px) {
          .sidebar {
            transform: translateX(calc(var(--sidebar-width) * -1));
          }

          .sidebar.open {
            transform: translateX(0);
          }

          .main-content {
            margin-left: 0;
          }

          .page-content {
            padding: 20px 15px;
          }
        }

        @media (max-width: 768px) {
          :root {
            --sidebar-width: 240px;
          }
          
          .sidebar {
            z-index: 101;
          }

          .top-navbar {
            padding: 0 15px;
          }

          .user-name {
            display: none;
          }

          .page-content {
            padding: 15px 10px;
          }
        }

        @media (max-width: 480px) {
          :root {
            --sidebar-width: 100%;
          }

          .logo-text {
            display: none;
          }

          .nav-text {
            display: none;
          }

          .nav-link {
            justify-content: center;
          }

          .nav-icon {
            margin-right: 0;
            font-size: 24px;
          }

          .dashboard-title {
            font-size: 22px;
          }

          .stats-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </>
  );
};

export default SidebarLayout;