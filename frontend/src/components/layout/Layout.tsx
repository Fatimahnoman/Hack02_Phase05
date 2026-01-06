import React from 'react';
import Header from './Header';
import Head from 'next/head';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <>
      <Head>
        <title>Evolution of Todo</title>
        <meta name="description" content="A modern todo application" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="layout">
        <Header />
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
          background-color: #f5f5f5;
          color: #333;
        }

        .layout {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }

        main {
          flex: 1;
          padding: 20px;
          max-width: 1200px;
          margin: 0 auto;
          width: 100%;
        }

        .container {
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
        }

        .auth-form {
          background: white;
          padding: 30px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .auth-form h2 {
          margin-bottom: 20px;
          text-align: center;
        }

        .auth-form div {
          margin-bottom: 15px;
        }

        .auth-form label {
          display: block;
          margin-bottom: 5px;
          font-weight: bold;
        }

        .auth-form input {
          width: 100%;
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 16px;
        }

        .auth-form button {
          width: 100%;
          padding: 12px;
          background-color: #0070f3;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 16px;
          cursor: pointer;
        }

        .auth-form button:hover {
          background-color: #0060e0;
        }

        .error {
          color: #e00;
          background-color: #ffe;
          padding: 10px;
          border-radius: 4px;
          margin-bottom: 15px;
          border: 1px solid #fcc;
        }

        @media (max-width: 768px) {
          main {
            padding: 10px;
          }

          .container {
            padding: 15px;
          }

          .auth-form {
            padding: 20px;
          }
        }
      `}</style>
    </>
  );
};

export default Layout;