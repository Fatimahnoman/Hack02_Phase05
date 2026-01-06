import React from 'react';
import Layout from '../components/layout/Layout';
import Link from 'next/link';

const HomePage = () => {
  return (
    <Layout>
      <div className="container">
        <div className="hero">
          <h1>Welcome to Evolution of Todo</h1>
          <p>A modern, full-featured todo application with authentication.</p>
          <div className="cta-buttons">
            <Link href="/signup">
              <button className="primary-btn">Get Started</button>
            </Link>
            <Link href="/signin">
              <button className="secondary-btn">Sign In</button>
            </Link>
          </div>
        </div>
      </div>
      <style jsx>{`
        .hero {
          text-align: center;
          padding: 60px 20px;
        }

        .hero h1 {
          font-size: 2.5rem;
          margin-bottom: 20px;
          color: #333;
        }

        .hero p {
          font-size: 1.2rem;
          color: #666;
          margin-bottom: 30px;
        }

        .cta-buttons {
          display: flex;
          justify-content: center;
          gap: 15px;
          flex-wrap: wrap;
        }

        .primary-btn, .secondary-btn {
          padding: 12px 24px;
          border-radius: 6px;
          font-size: 1rem;
          cursor: pointer;
          text-decoration: none;
          display: inline-block;
        }

        .primary-btn {
          background-color: #0070f3;
          color: white;
          border: none;
        }

        .primary-btn:hover {
          background-color: #0060e0;
        }

        .secondary-btn {
          background-color: white;
          color: #0070f3;
          border: 1px solid #0070f3;
        }

        .secondary-btn:hover {
          background-color: #f0f8ff;
        }

        @media (max-width: 768px) {
          .hero h1 {
            font-size: 2rem;
          }

          .hero p {
            font-size: 1rem;
          }

          .cta-buttons {
            flex-direction: column;
            align-items: center;
          }

          .primary-btn, .secondary-btn {
            width: 200px;
          }
        }
      `}</style>
    </Layout>
  );
};

export default HomePage;