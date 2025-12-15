import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import { AuthProvider, useAuth, SigninForm } from '../components/Auth';

function SigninPageContent() {
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    // Redirect if already authenticated
    if (isAuthenticated && !isLoading) {
      window.location.href = '/';
    }
  }, [isAuthenticated, isLoading]);

  const handleSuccess = () => {
    // Redirect to saved destination or home after successful signin
    const redirectUrl = sessionStorage.getItem('redirectAfterLogin') || '/';
    sessionStorage.removeItem('redirectAfterLogin');
    window.location.href = redirectUrl;
  };

  const handleSwitchToSignup = () => {
    window.location.href = '/signup';
  };

  if (isLoading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        Loading...
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        Redirecting...
      </div>
    );
  }

  return (
    <SigninForm
      onSuccess={handleSuccess}
      onSwitchToSignup={handleSwitchToSignup}
    />
  );
}

export default function SigninPage() {
  return (
    <AuthProvider>
      <Layout
        title="Sign In"
        description="Sign in to AI-Native Robotics Textbook"
      >
        <SigninPageContent />
      </Layout>
    </AuthProvider>
  );
}
