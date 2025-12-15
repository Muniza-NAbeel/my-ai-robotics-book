import React from 'react';
import { AuthProvider, ProtectedRoute } from '../components/Auth';
import Chatbot from '../components/Chatbot';

export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ProtectedRoute>
        {children}
      </ProtectedRoute>
      <Chatbot />
    </AuthProvider>
  );
}
