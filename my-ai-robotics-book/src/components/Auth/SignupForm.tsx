import React, { useState } from 'react';
import { useAuth } from './AuthProvider';
import { Questionnaire } from './Questionnaire';
import styles from './Auth.module.css';

interface SignupFormProps {
  onSuccess?: () => void;
  onSwitchToSignin?: () => void;
}

export function SignupForm({ onSuccess, onSwitchToSignin }: SignupFormProps) {
  const { signup } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<{ [key: string]: string }>({});

  const [softwareBackground, setSoftwareBackground] = useState({
    programming_level: 'beginner' as const,
    languages_known: [] as string[],
    ai_experience: 'none' as const,
    web_dev_experience: 'none' as const,
  });

  const [hardwareBackground, setHardwareBackground] = useState({
    robotics_experience: false,
    electronics_familiarity: 'none' as const,
    hardware_access: [] as string[],
  });

  const validateForm = (): boolean => {
    const errors: { [key: string]: string } = {};

    // Email validation
    if (!email) {
      errors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = 'Invalid email format';
    }

    // Password validation
    if (!password) {
      errors.password = 'Password is required';
    } else if (password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    } else if (!/[A-Z]/.test(password)) {
      errors.password = 'Password must contain an uppercase letter';
    } else if (!/[a-z]/.test(password)) {
      errors.password = 'Password must contain a lowercase letter';
    } else if (!/[0-9]/.test(password)) {
      errors.password = 'Password must contain a number';
    }

    // Confirm password
    if (password !== confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    // Questionnaire validation
    if (softwareBackground.languages_known.length === 0) {
      errors.languages_known = 'Select at least one language';
    }

    if (hardwareBackground.hardware_access.length === 0) {
      errors.hardware_access = 'Select at least one hardware option';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      setError('Please fill all required fields correctly');
      return;
    }

    setIsLoading(true);

    try {
      const result = await signup({
        email,
        password,
        software_background: softwareBackground,
        hardware_background: hardwareBackground,
      });

      if (result.success) {
        onSuccess?.();
      } else {
        setError(result.error || 'Signup failed');
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
        <h2 className={styles.title}>Create Account</h2>
        <p className={styles.subtitle}>
          Join our AI-Native Robotics learning platform
        </p>

        {error && <div className={styles.errorAlert}>{error}</div>}

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.field}>
            <label className={styles.label}>Email *</label>
            <input
              type="email"
              className={styles.input}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={isLoading}
            />
            {fieldErrors.email && (
              <span className={styles.error}>{fieldErrors.email}</span>
            )}
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Password *</label>
            <input
              type="password"
              className={styles.input}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Min 8 chars, uppercase, lowercase, number"
              disabled={isLoading}
            />
            {fieldErrors.password && (
              <span className={styles.error}>{fieldErrors.password}</span>
            )}
          </div>

          <div className={styles.field}>
            <label className={styles.label}>Confirm Password *</label>
            <input
              type="password"
              className={styles.input}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              disabled={isLoading}
            />
            {fieldErrors.confirmPassword && (
              <span className={styles.error}>{fieldErrors.confirmPassword}</span>
            )}
          </div>

          <Questionnaire
            softwareBackground={softwareBackground}
            hardwareBackground={hardwareBackground}
            onSoftwareChange={setSoftwareBackground}
            onHardwareChange={setHardwareBackground}
            errors={fieldErrors}
          />

          <button
            type="submit"
            className={styles.submitButton}
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className={styles.switchAuth}>
          Already have an account?{' '}
          <button
            type="button"
            className={styles.linkButton}
            onClick={onSwitchToSignin}
          >
            Sign In
          </button>
        </div>
      </div>
    </div>
  );
}

export default SignupForm;
