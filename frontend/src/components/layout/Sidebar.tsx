import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';

const Sidebar = () => {
  const [width, setWidth] = useState(280);
  const [isResizing, setIsResizing] = useState(false);
  const sidebarRef = useRef<HTMLDivElement>(null);
  const { user, logout, isAuthenticated } = useAuth();

  const MIN_WIDTH = 150;
  const MAX_WIDTH = 500;

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (!isResizing) return;

    const containerRect = sidebarRef.current?.getBoundingClientRect();
    if (!containerRect) return;

    const newWidth = e.clientX - containerRect.left;
    const clampedWidth = Math.max(MIN_WIDTH, Math.min(MAX_WIDTH, newWidth));

    if (clampedWidth !== width) {
      setWidth(clampedWidth);

      // Dispatch custom event to notify layout of width change
      window.dispatchEvent(new CustomEvent('sidebarResize', {
        detail: { width: clampedWidth }
      }));
    }
  };

  const handleMouseUp = () => {
    setIsResizing(false);
  };

  useEffect(() => {
    const handleGlobalMouseMove = (e: MouseEvent) => handleMouseMove(e);
    const handleGlobalMouseUp = () => handleMouseUp();

    if (isResizing) {
      document.addEventListener('mousemove', handleGlobalMouseMove);
      document.addEventListener('mouseup', handleGlobalMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleGlobalMouseMove);
      document.removeEventListener('mouseup', handleGlobalMouseUp);
    };
  }, [isResizing]);

  const handleLogout = () => {
    logout();
  };

  return (
    <aside className="sidebar" ref={sidebarRef} style={{ width: `${width}px`, minWidth: `${width}px` }}>
      <div className="sidebar-content">
        <Link href="/">
          <h1 className="sidebar-logo">Evolution of Todo</h1>
        </Link>

        <nav className="sidebar-nav">
          {isAuthenticated ? (
            <>
              <Link href="/dashboard" legacyBehavior>
                <a className="sidebar-link">Dashboard</a>
              </Link>
              <div className="sidebar-user-info">
                Welcome, {user?.email}
              </div>
              <button onClick={handleLogout} className="sidebar-logout-btn">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/signin" legacyBehavior>
                <a className="sidebar-link">Sign In</a>
              </Link>
              <Link href="/signup" legacyBehavior>
                <a className="sidebar-link">Sign Up</a>
              </Link>
            </>
          )}
        </nav>
      </div>

      <div
        className="resize-handle"
        onMouseDown={handleMouseDown}
        style={{
          position: 'absolute',
          right: 0,
          top: 0,
          bottom: 0,
          width: '6px',
          cursor: 'col-resize',
          zIndex: 1000,
          background: 'rgba(255, 255, 255, 0.3)',
        }}
      />

      <style jsx>{`
        .sidebar {
          height: 100vh;
          position: fixed;
          left: 0;
          top: 0;
          background: linear-gradient(135deg, #000000 0%, #333333 100%);
          box-shadow: 4px 0 20px rgba(0, 0, 0, 0.2);
          z-index: 999;
          display: flex;
          flex-direction: column;
          padding: 20px 0;
          transition: width 0.1s ease;
        }

        .sidebar-content {
          flex: 1;
          display: flex;
          flex-direction: column;
          padding: 0 15px;
        }

        .sidebar-logo {
          color: white;
          font-size: 1.5rem;
          font-weight: 700;
          text-align: center;
          margin: 0 0 30px 0;
          padding: 0 10px;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
          cursor: pointer;
          transition: transform 0.2s ease;
        }

        .sidebar-logo:hover {
          transform: scale(1.05);
          text-decoration: none;
        }

        .sidebar-nav {
          display: flex;
          flex-direction: column;
          gap: 15px;
          flex: 1;
        }

        .sidebar-link {
          display: block;
          color: white;
          padding: 12px 16px;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 500;
          transition: all 0.3s ease;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.15);
          text-align: center;
        }

        .sidebar-link:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateX(5px);
        }

        .sidebar-user-info {
          color: white;
          padding: 12px 16px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          font-weight: 500;
          text-align: center;
          border: 1px solid rgba(255, 255, 255, 0.15);
          margin: 10px 0;
        }

        .sidebar-logout-btn {
          width: 100%;
          padding: 12px 16px;
          background: rgba(255, 255, 255, 0.1);
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.15);
          border-radius: 8px;
          cursor: pointer;
          font-weight: 500;
          transition: all 0.3s ease;
          text-align: center;
        }

        .sidebar-logout-btn:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateX(5px);
        }

        .resize-handle {
          position: absolute;
          right: 0;
          top: 0;
          bottom: 0;
          width: 6px;
          cursor: col-resize;
          z-index: 1000;
          background: rgba(255, 255, 255, 0.3);
          transition: background 0.2s ease;
        }

        .resize-handle:hover {
          background: rgba(255, 255, 255, 0.5);
        }

        @media (max-width: 768px) {
          .sidebar {
            width: 70px;
            min-width: 70px;
          }

          .resize-handle {
            display: none;
          }

          .sidebar-logo {
            font-size: 1rem;
            writing-mode: vertical-rl;
            text-orientation: mixed;
            white-space: nowrap;
            margin: 10px 0;
          }

          .sidebar-link,
          .sidebar-user-info,
          .sidebar-logout-btn {
            padding: 15px 8px;
            font-size: 0.8rem;
            writing-mode: vertical-rl;
            text-orientation: mixed;
            white-space: nowrap;
          }
        }
      `}</style>
    </aside>
  );
};

export default Sidebar;