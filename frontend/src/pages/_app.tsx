import React from 'react';
import { AppProps } from 'next/app';
import { AuthProvider } from '../contexts/AuthContext';
import SidebarLayout from '../components/layout/SidebarLayout';
import '../styles/animations.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <SidebarLayout>
        <Component {...pageProps} />
      </SidebarLayout>
    </AuthProvider>
  );
}

export default MyApp;