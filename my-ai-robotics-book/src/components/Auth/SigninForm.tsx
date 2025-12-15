import React, { useState } from 'react';
import { useAuth } from './AuthProvider';
import styles from './Auth.module.css';

interface SigninFormProps {
  onSuccess?: () => void;
  onSwitchToSignup?: () => void;
}

export function SigninForm({ onSuccess, onSwitchToSignup }: SigninFormProps) {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError('Please enter email and password');
      return;
    }

    setIsLoading(true);

    try {
      const result = await login(email, password);

      if (result.success) {
        onSuccess?.();
      } else {
        setError(result.error || 'Invalid email or password');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <h2 className={styles.title}>Welcome Back</h2>
        <p className={styles.subtitle}>
          Sign in to continue your learning journey
        </p>

        {error && <div className={styles.errorAlert}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.field}>
            <label className={styles.label}>Email</label>
            <input
              type="email"
              className={styles.input}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={isLoading}
            />
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Password</label>
            <input
              type="password"
              className={styles.input}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            className={styles.submitButton}
            disabled={isLoading}
          >
            {isLoading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className={styles.switchAuth}>
          Don't have an account?{' '}
          <button
            type="button"
            className={styles.linkButton}
            onClick={onSwitchToSignup}
          >
            Create Account
          </button>
        </div>
      </div>
    </div>
  );
}

export default SigninForm;
