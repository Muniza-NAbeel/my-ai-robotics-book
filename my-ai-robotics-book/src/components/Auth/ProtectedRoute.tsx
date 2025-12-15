import React, { useState, useEffect } from 'react';
import { useAuth } from './AuthProvider';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

// Check if we're in browser and on docs route
const getInitialDocsRoute = () => {
  if (typeof window !== 'undefined') {
    return window.location.pathname.startsWith('/docs');
  }
  return false;
};

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const [isDocsRoute] = useState(getInitialDocsRoute);
  const [authCheckDone, setAuthCheckDone] = useState(false);

  useEffect(() => {
    if (!isLoading) {
      setAuthCheckDone(true);
    }
  }, [isLoading]);

  // Server-side render - just show children
  if (typeof window === 'undefined') {
    return <>{children}</>;
  }

  // Not a docs route - show content immediately
  if (!isDocsRoute) {
    return <>{children}</>;
  }

  // Docs route - wait for auth check
  if (!authCheckDone) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '80vh'
      }}>
        <p>Checking access...</p>
      </div>
    );
  }

  // Docs route + not authenticated = show restricted message
  if (!isAuthenticated) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '80vh',
        padding: '2rem',
        textAlign: 'center',
        backgroundColor: '#f5f5f5'
      }}>
        <div style={{
          backgroundColor: 'white',
          padding: '3rem',
          borderRadius: '12px',
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
          maxWidth: '450px'
        }}>
          <h2 style={{ marginBottom: '1rem', color: '#333' }}>Access Restricted</h2>
          <p style={{ marginBottom: '2rem', color: '#666', fontSize: '1.1rem' }}>
            Please create an account or sign in to access the book content.
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <a
              href="/signup"
              style={{
                padding: '0.875rem 2rem',
                backgroundColor: '#2e8555',
                color: 'white',
                borderRadius: '6px',
                textDecoration: 'none',
                fontWeight: 'bold',
                fontSize: '1rem'
              }}
            >
              Sign Up
            </a>
            <a
              href="/signin"
              style={{
                padding: '0.875rem 2rem',
                backgroundColor: '#1a1a1a',
                color: 'white',
                borderRadius: '6px',
                textDecoration: 'none',
                fontWeight: 'bold',
                fontSize: '1rem'
              }}
            >
              Sign In
            </a>
          </div>
        </div>
      </div>
    );
  }

  // Docs route + authenticated = show content
  return <>{children}</>;
}

export default ProtectedRoute;
