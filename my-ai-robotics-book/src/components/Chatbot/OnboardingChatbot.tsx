/**
 * OnboardingChatbot - Conversational signup flow
 *
 * This component guides new users through account creation via chatbot.
 * Flow: Enter credentials -> Chatbot asks background questions -> Account created
 *
 * WHY chatbot instead of forms:
 * - More engaging user experience
 * - Natural conversation feels like talking to a tutor
 * - Ensures complete data collection
 * - Core innovation for hackathon bonus points
 */

import React, { useState, useCallback, useRef, useEffect } from 'react';
import styles from './Chatbot.module.css';

const API_BASE_URL = 'http://localhost:8000';
const STORAGE_KEY = 'onboarding_session';

// Saved session state structure for localStorage
interface SavedSessionState {
  sessionId: string;
  email: string;
  timestamp: number;
}

interface QuestionOption {
  value: string;
  label: string;
  description?: string;
}

interface Question {
  id: string;
  type: 'greeting' | 'single_select' | 'multi_select' | 'confirmation';
  bot_message: string;
  options?: QuestionOption[];
  summary?: string;
  collected_answers?: Record<string, unknown>;
}

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  question?: Question;
}

interface OnboardingChatbotProps {
  onSuccess: () => void;
  onSwitchToSignin: () => void;
}

// Password validation matching backend requirements
function validatePassword(password: string): string[] {
  const errors: string[] = [];
  if (password.length < 8) errors.push('At least 8 characters');
  if (!/[A-Z]/.test(password)) errors.push('One uppercase letter');
  if (!/[a-z]/.test(password)) errors.push('One lowercase letter');
  if (!/[0-9]/.test(password)) errors.push('One number');
  return errors;
}

function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export default function OnboardingChatbot({ onSuccess, onSwitchToSignin }: OnboardingChatbotProps) {
  // Credentials state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [credentialsError, setCredentialsError] = useState('');

  // Onboarding state
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showCredentialsForm, setShowCredentialsForm] = useState(true);
  const [isRecovering, setIsRecovering] = useState(true); // Start true to check for saved session

  // Multi-select state
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);

  const chatEndRef = useRef<HTMLDivElement>(null);

  // Save session to localStorage
  const saveSession = useCallback((sid: string, userEmail: string) => {
    const state: SavedSessionState = {
      sessionId: sid,
      email: userEmail,
      timestamp: Date.now(),
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
      console.warn('Failed to save onboarding session to localStorage:', e);
    }
  }, []);

  // Clear saved session from localStorage
  const clearSavedSession = useCallback(() => {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {
      console.warn('Failed to clear saved session:', e);
    }
  }, []);

  // Check for and recover saved session on mount
  useEffect(() => {
    const recoverSession = async () => {
      try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (!saved) {
          setIsRecovering(false);
          return;
        }

        const state: SavedSessionState = JSON.parse(saved);

        // Check if session is less than 25 minutes old (backend expiry is 30 min)
        const ageMinutes = (Date.now() - state.timestamp) / 1000 / 60;
        if (ageMinutes > 25) {
          console.log('Saved session too old, clearing...');
          clearSavedSession();
          setIsRecovering(false);
          return;
        }

        // Try to get current question from backend to validate session
        const response = await fetch(
          `${API_BASE_URL}/api/auth/onboarding/question/${state.sessionId}`,
          { credentials: 'include' }
        );

        if (!response.ok) {
          // Session expired or invalid
          console.log('Saved session invalid, clearing...');
          clearSavedSession();
          setIsRecovering(false);
          return;
        }

        const data = await response.json();

        // Session is valid - restore state
        setSessionId(state.sessionId);
        setEmail(state.email);
        setShowCredentialsForm(false);

        // Add recovery message and current question
        const recoveryMessages: Message[] = [
          {
            id: Date.now() - 1,
            text: `Welcome back! Let's continue where we left off.`,
            sender: 'bot',
          },
          {
            id: Date.now(),
            text: data.current_question.bot_message,
            sender: 'bot',
            question: data.current_question,
          },
        ];
        setMessages(recoveryMessages);
        setCurrentQuestion(data.current_question);

      } catch (e) {
        console.warn('Session recovery failed:', e);
        clearSavedSession();
      } finally {
        setIsRecovering(false);
      }
    };

    recoverSession();
  }, [clearSavedSession]);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentQuestion]);

  // Start onboarding after credentials validation
  const handleStartOnboarding = useCallback(async () => {
    // Client-side validation
    if (!validateEmail(email)) {
      setCredentialsError('Please enter a valid email address');
      return;
    }

    const passwordErrors = validatePassword(password);
    if (passwordErrors.length > 0) {
      setCredentialsError(`Password needs: ${passwordErrors.join(', ')}`);
      return;
    }

    if (password !== confirmPassword) {
      setCredentialsError('Passwords do not match');
      return;
    }

    setCredentialsError('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/onboarding/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setCredentialsError(data.message || 'Failed to start signup');
        return;
      }

      // Success - switch to chat mode
      setSessionId(data.session_id);
      setShowCredentialsForm(false);

      // Save session to localStorage for recovery
      saveSession(data.session_id, email);

      // Add welcome message
      if (data.current_question) {
        setMessages([{
          id: Date.now(),
          text: data.current_question.bot_message,
          sender: 'bot',
          question: data.current_question,
        }]);
        setCurrentQuestion(data.current_question);
      }
    } catch (error) {
      console.error('Start onboarding error:', error);
      setCredentialsError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [email, password, confirmPassword, saveSession]);

  // Submit answer and get next question
  const submitAnswer = useCallback(async (answer: string | string[]) => {
    if (!sessionId) return;

    // Add user's answer as message
    const answerText = Array.isArray(answer) ? answer.join(', ') : answer;
    setMessages(prev => [...prev, {
      id: Date.now(),
      text: answerText,
      sender: 'user',
    }]);

    setIsLoading(true);
    setCurrentQuestion(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/onboarding/answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ session_id: sessionId, answer }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessages(prev => [...prev, {
          id: Date.now(),
          text: data.message || 'Something went wrong. Please try again.',
          sender: 'bot',
        }]);
        return;
      }

      // Small delay for typing effect
      await new Promise(resolve => setTimeout(resolve, 500));

      if (data.status === 'continue' && data.next_question) {
        setMessages(prev => [...prev, {
          id: Date.now(),
          text: data.next_question.bot_message,
          sender: 'bot',
          question: data.next_question,
        }]);
        setCurrentQuestion(data.next_question);
        setSelectedOptions([]);
      } else if (data.status === 'complete') {
        // All questions answered - show summary
        const summaryResponse = await fetch(
          `${API_BASE_URL}/api/auth/onboarding/summary/${sessionId}`,
          { credentials: 'include' }
        );
        const summaryData = await summaryResponse.json();

        setMessages(prev => [...prev, {
          id: Date.now(),
          text: "Here's a summary of your profile:",
          sender: 'bot',
          question: {
            id: 'summary',
            type: 'confirmation',
            bot_message: "Here's a summary of your profile:",
            summary: summaryData.summary_text,
            collected_answers: summaryData.collected_answers,
          },
        }]);
        setCurrentQuestion({
          id: 'summary',
          type: 'confirmation',
          bot_message: "Here's a summary of your profile:",
          summary: summaryData.summary_text,
          collected_answers: summaryData.collected_answers,
        });
      }
    } catch (error) {
      console.error('Submit answer error:', error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: 'Network error. Please try again.',
        sender: 'bot',
      }]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  // Complete signup
  const handleCompleteSignup = useCallback(async () => {
    if (!sessionId) return;

    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/onboarding/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ session_id: sessionId }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessages(prev => [...prev, {
          id: Date.now(),
          text: data.message || 'Failed to create account. Please try again.',
          sender: 'bot',
        }]);
        return;
      }

      // Clear saved session on successful completion
      clearSavedSession();

      // Success message
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: `Welcome aboard, ${data.user.name}! Your personalized learning experience awaits.`,
        sender: 'bot',
      }]);

      // Clear current question to hide buttons
      setCurrentQuestion(null);

      // Redirect after short delay
      setTimeout(() => {
        onSuccess();
      }, 1500);
    } catch (error) {
      console.error('Complete signup error:', error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: 'Network error. Please try again.',
        sender: 'bot',
      }]);
    } finally {
      setIsLoading(false);
    }
  }, [sessionId, onSuccess, clearSavedSession]);

  // Handle single select option click
  const handleSingleSelect = useCallback((value: string, label: string) => {
    submitAnswer(value);
  }, [submitAnswer]);

  // Handle multi-select toggle
  const toggleMultiSelect = useCallback((value: string) => {
    setSelectedOptions(prev => {
      if (prev.includes(value)) {
        return prev.filter(v => v !== value);
      }
      // If selecting "none", clear others
      if (value === 'none') {
        return ['none'];
      }
      // If selecting something else while "none" is selected, remove "none"
      return [...prev.filter(v => v !== 'none'), value];
    });
  }, []);

  // Submit multi-select
  const handleMultiSelectSubmit = useCallback(() => {
    if (selectedOptions.length === 0) return;
    submitAnswer(selectedOptions);
  }, [selectedOptions, submitAnswer]);

  // Handle greeting (just continue to next)
  const handleGreetingContinue = useCallback(() => {
    submitAnswer('continue');
  }, [submitAnswer]);

  // Restart onboarding (for edit option)
  const handleRestart = useCallback(() => {
    clearSavedSession();
    setShowCredentialsForm(true);
    setSessionId(null);
    setMessages([]);
    setCurrentQuestion(null);
    setSelectedOptions([]);
  }, [clearSavedSession]);

  // Show loading while checking for saved session
  if (isRecovering) {
    return (
      <div className={styles.onboardingContainer}>
        <div className={styles.onboardingCard}>
          <div className={styles.onboardingHeader}>
            <h2>Loading...</h2>
            <p>Checking for saved progress</p>
          </div>
          <div className={styles.typingIndicator} style={{ justifyContent: 'center', marginTop: '20px' }}>
            <div className={styles.typingDot} />
            <div className={styles.typingDot} />
            <div className={styles.typingDot} />
          </div>
        </div>
      </div>
    );
  }

  // Render credentials form
  if (showCredentialsForm) {
    return (
      <div className={styles.onboardingContainer}>
        <div className={styles.onboardingCard}>
          <div className={styles.onboardingHeader}>
            <h2>Create Your Account</h2>
            <p>Join the AI-Native Robotics learning experience</p>
          </div>

          <form className={styles.credentialsForm} onSubmit={(e) => { e.preventDefault(); handleStartOnboarding(); }}>
            <div className={styles.formGroup}>
              <label>Email Address</label>
              <input
                type="email"
                className={styles.formInput}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                disabled={isLoading}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Password</label>
              <input
                type="password"
                className={styles.formInput}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Create a password"
                disabled={isLoading}
              />
            </div>

            <div className={styles.formGroup}>
              <label>Confirm Password</label>
              <input
                type="password"
                className={styles.formInput}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
                disabled={isLoading}
              />
            </div>

            {credentialsError && (
              <div className={styles.formError}>{credentialsError}</div>
            )}

            <button
              type="submit"
              className={styles.continueButton}
              disabled={isLoading || !email || !password || !confirmPassword}
            >
              {isLoading ? 'Starting...' : 'Continue'}
            </button>
          </form>

          <div className={styles.signinLink}>
            Already have an account?{' '}
            <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToSignin(); }}>
              Sign in
            </a>
          </div>
        </div>
      </div>
    );
  }

  // Render chatbot conversation
  return (
    <div className={styles.onboardingContainer}>
      <div className={styles.onboardingCard}>
        <div className={styles.onboardingHeader}>
          <h2>Let&apos;s Personalize Your Experience</h2>
          <p>Answer a few questions so we can tailor your learning journey</p>
        </div>

        <div className={styles.chatSection}>
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`${styles.onboardingMessage} ${styles[msg.sender]}`}
            >
              {msg.text}
            </div>
          ))}

          {/* Typing indicator */}
          {isLoading && (
            <div className={styles.typingIndicator}>
              <div className={styles.typingDot} />
              <div className={styles.typingDot} />
              <div className={styles.typingDot} />
            </div>
          )}

          {/* Current question options */}
          {currentQuestion && !isLoading && (
            <>
              {/* Greeting - just a continue button */}
              {currentQuestion.type === 'greeting' && (
                <button
                  className={styles.continueButton}
                  onClick={handleGreetingContinue}
                  style={{ marginTop: '12px', maxWidth: '200px' }}
                >
                  Let&apos;s Go!
                </button>
              )}

              {/* Single select options */}
              {currentQuestion.type === 'single_select' && currentQuestion.options && (
                <div className={styles.optionsGrid}>
                  {currentQuestion.options.map((option) => (
                    <button
                      key={option.value}
                      className={styles.optionButton}
                      onClick={() => handleSingleSelect(option.value, option.label)}
                    >
                      <span className={styles.optionLabel}>{option.label}</span>
                      {option.description && (
                        <span className={styles.optionDescription}>
                          {option.description}
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              )}

              {/* Multi select options */}
              {currentQuestion.type === 'multi_select' && currentQuestion.options && (
                <>
                  <div className={styles.multiSelectGrid}>
                    {currentQuestion.options.map((option) => (
                      <button
                        key={option.value}
                        className={`${styles.multiSelectOption} ${
                          selectedOptions.includes(option.value) ? styles.selected : ''
                        }`}
                        onClick={() => toggleMultiSelect(option.value)}
                      >
                        <span className={`${styles.checkbox} ${
                          selectedOptions.includes(option.value) ? styles.checked : ''
                        }`}>
                          {selectedOptions.includes(option.value) && '✓'}
                        </span>
                        {option.label}
                      </button>
                    ))}
                  </div>
                  <button
                    className={styles.submitMultiSelect}
                    onClick={handleMultiSelectSubmit}
                    disabled={selectedOptions.length === 0}
                  >
                    Continue
                  </button>
                </>
              )}

              {/* Confirmation summary */}
              {currentQuestion.type === 'confirmation' && (
                <>
                  <div className={styles.summaryBox}>
                    <div className={styles.summaryText}>
                      {currentQuestion.summary}
                    </div>
                  </div>
                  <div className={styles.confirmButtons}>
                    <button
                      className={`${styles.confirmButton} ${styles.secondary}`}
                      onClick={handleRestart}
                    >
                      Edit
                    </button>
                    <button
                      className={`${styles.confirmButton} ${styles.primary}`}
                      onClick={handleCompleteSignup}
                    >
                      Create Account
                    </button>
                  </div>
                </>
              )}
            </>
          )}

          <div ref={chatEndRef} />
        </div>
      </div>
    </div>
  );
}
