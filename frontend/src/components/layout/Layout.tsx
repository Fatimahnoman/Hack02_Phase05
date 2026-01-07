import React, { useEffect } from 'react';
import Sidebar from './Sidebar';
import Head from 'next/head';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  useEffect(() => {
    // Listen for custom event from sidebar to update main content margin
    const handleSidebarResize = (event: CustomEvent) => {
      const sidebarWidth = event.detail.width;
      const mainElement = document.querySelector('main');
      if (mainElement) {
        mainElement.style.marginLeft = `${sidebarWidth}px`;
      }
    };

    window.addEventListener('sidebarResize', handleSidebarResize as EventListener);

    return () => {
      window.removeEventListener('sidebarResize', handleSidebarResize as EventListener);
    };
  }, []);

  return (
    <>
      <Head>
        <title>Evolution of Todo</title>
        <meta name="description" content="A modern todo application" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="layout">
        <Sidebar />
        <main>{children}</main>
      </div>
      <style jsx global>{`
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }

        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
            Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
          background: linear-gradient(135deg, #f0f4f8 0%, #c9e0f3 100%);
          color: #2d3748;
          min-height: 100vh;
          background-attachment: fixed;
        }

        .layout {
          min-height: 100vh;
          display: flex;
          flex-direction: row;
        }

        main {
          flex: 1;
          padding: 30px 20px;
          max-width: 1200px;
          margin: 0 auto;
          width: 100%;
          margin-left: 280px; /* Default width, will be overridden by JavaScript */
        }

        @media (max-width: 768px) {
          main {
            margin-left: 70px;
          }
        }

        .container {
          max-width: 600px;
          margin: 0 auto;
          padding: 25px;
          background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
          margin-top: 20px;
        }

        .auth-form {
          background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
          padding: 35px;
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
          border: 1px solid rgba(255, 255, 255, 0.2);
          backdrop-filter: blur(10px);
        }

        .auth-form h2 {
          margin-bottom: 25px;
          text-align: center;
          font-size: 1.8rem;
          font-weight: 700;
          color: #2d3748;
          background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .auth-form div {
          margin-bottom: 20px;
        }

        .auth-form label {
          display: block;
          margin-bottom: 8px;
          font-weight: 600;
          color: #4a5568;
          font-size: 1rem;
        }

        .auth-form input {
          width: 100%;
          padding: 14px 18px;
          border: 2px solid #e2e8f0;
          border-radius: 12px;
          font-size: 16px;
          transition: all 0.3s ease;
          background: white;
          box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
        }

        .auth-form input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .auth-form button {
          width: 100%;
          padding: 16px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          border-radius: 12px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          letter-spacing: 0.5px;
          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .auth-form button:hover {
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
          transform: translateY(-3px);
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        .error {
          color: white;
          background: linear-gradient(135deg, #fa5252 0%, #f5365c 100%);
          padding: 14px 18px;
          border-radius: 10px;
          margin-bottom: 20px;
          border: 1px solid rgba(255, 255, 255, 0.2);
          font-weight: 500;
          box-shadow: 0 4px 15px rgba(250, 82, 82, 0.3);
        }

        @media (max-width: 768px) {
          main {
            padding: 20px 15px;
          }

          .container {
            padding: 20px 15px;
            margin-top: 15px;
          }

          .auth-form {
            padding: 25px 20px;
          }

          .auth-form h2 {
            font-size: 1.5rem;
          }
        }
      `}</style>
    </>
  );
};

export default Layout;