import React from 'react';
import SigninForm from '../components/auth/SigninForm';
import Layout from '../components/layout/Layout';

const SigninPage = () => {
  return (
    <Layout>
      <div className="container">
        <SigninForm />
      </div>
    </Layout>
  );
};

export default SigninPage;