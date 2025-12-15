import React, { useState } from 'react';
import { useAuth } from './AuthProvider';
import styles from './Auth.module.css';

interface LogoutButtonProps {
  onLogout?: () => void;
  className?: string;
}

export function LogoutButton({ onLogout, className }: LogoutButtonProps) {
  const { logout, isAuthenticated } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  if (!isAuthenticated) {
    return null;
  }

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await logout();
      onLogout?.();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleLogout}
      className={className || styles.logoutButton}
      disabled={isLoading}
    >
      {isLoading ? 'Logging out...' : 'Logout'}
    </button>
  );
}

export default LogoutButton;
