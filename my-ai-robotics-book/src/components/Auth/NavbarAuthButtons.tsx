/**
 * Navbar Authentication Buttons
 *
 * Shows different UI based on auth state:
 * - Guest: "Sign In" button only (Get Started is in hero section)
 * - Authenticated: User name dropdown with "Sign Out"
 */

import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from './AuthProvider';
import styles from './NavbarAuth.module.css';

export function NavbarAuthButtons() {
  const { isAuthenticated, isLoading, user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleLogout = async () => {
    await logout();
    // Redirect to home page after logout
    window.location.href = '/';
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (isLoading) {
    return <div className={styles.loading}>...</div>;
  }

  if (isAuthenticated && user) {
    const displayName = user.name || user.email.split('@')[0];

    return (
      <div className={styles.authButtons}>
        <div
          ref={dropdownRef}
          className={styles.userDropdown}
          onMouseEnter={() => setShowDropdown(true)}
          onMouseLeave={() => setShowDropdown(false)}
          onClick={() => setShowDropdown(!showDropdown)}
        >
          <span className={styles.userName}>
            {displayName}
          </span>
          {showDropdown && (
            <div className={styles.dropdownMenu}>
              <span className={styles.dropdownEmail}>{user.email}</span>
              <hr className={styles.dropdownDivider} />
              <button
                onClick={handleLogout}
                className={styles.dropdownItem}
              >
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={styles.authButtons}>
      <a href="/signin" className={styles.loginButton}>
        Sign In
      </a>
    </div>
  );
}

export default NavbarAuthButtons;
