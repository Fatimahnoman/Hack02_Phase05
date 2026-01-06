import React from 'react';
import SignupForm from '../components/auth/SignupForm';
import Layout from '../components/layout/Layout';

const SignupPage = () => {
  return (
    <Layout>
      <div className="container">
        <SignupForm />
      </div>
    </Layout>
  );
};

export default SignupPage;