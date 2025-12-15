/**
 * Signup Page with Chatbot-Driven Onboarding
 *
 * This page uses OnboardingChatbot for a conversational signup experience.
 * The chatbot collects user background information through natural conversation,
 * which is the core innovation for the hackathon (50 bonus points).
 *
 * Flow:
 * 1. User enters email/password
 * 2. Chatbot guides them through background questions
 * 3. Account created with complete profile
 * 4. Immediate personalization begins
 */

import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import { AuthProvider, useAuth } from '../components/Auth';
import OnboardingChatbot from '../components/Chatbot/OnboardingChatbot';

function SignupPageContent() {
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    // Redirect if already authenticated
    if (isAuthenticated && !isLoading) {
      window.location.href = '/';
    }
  }, [isAuthenticated, isLoading]);

  const handleSuccess = () => {
    // Redirect to intro page after successful signup
    // The chatbot has already collected all profile data
    const redirectUrl = sessionStorage.getItem('redirectAfterLogin') || '/docs/intro-foundations/intro';
    sessionStorage.removeItem('redirectAfterLogin');
    window.location.href = redirectUrl;
  };

  const handleSwitchToSignin = () => {
    window.location.href = '/signin';
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

  // Use OnboardingChatbot for conversational signup
  return (
    <OnboardingChatbot
      onSuccess={handleSuccess}
      onSwitchToSignin={handleSwitchToSignin}
    />
  );
}

export default function SignupPage() {
  return (
    <AuthProvider>
      <Layout
        title="Create Account"
        description="Sign up for AI-Native Robotics Textbook with personalized onboarding"
      >
        <SignupPageContent />
      </Layout>
    </AuthProvider>
  );
}
