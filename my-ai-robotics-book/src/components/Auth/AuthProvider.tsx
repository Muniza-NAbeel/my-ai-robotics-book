import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { authClient } from '../../lib/auth-client';

// API URL - using Hugging Face Space backend
const FASTAPI_URL = 'https://muniza-nabeel-hackathon.hf.space';

interface User {
  user_id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  signup: (data: SignupData) => Promise<{ success: boolean; error?: string }>;
  checkAuth: () => Promise<void>;
}

interface SoftwareBackground {
  programming_level: 'beginner' | 'intermediate' | 'advanced';
  languages_known: string[];
  ai_experience: 'none' | 'basic' | 'intermediate' | 'advanced';
  web_dev_experience: 'none' | 'basic' | 'intermediate' | 'advanced';
}

interface HardwareBackground {
  robotics_experience: boolean;
  electronics_familiarity: 'none' | 'basic' | 'intermediate';
  hardware_access: string[];
}

interface SignupData {
  email: string;
  password: string;
  software_background: SoftwareBackground;
  hardware_background: HardwareBackground;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const checkAuth = useCallback(async () => {
    try {
      const session = await authClient.getSession();

      if (session?.data?.user) {
        setUser({
          user_id: session.data.user.id,
          email: session.data.user.email,
          name: session.data.user.name
        });
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const login = async (email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      const result = await authClient.signIn.email({ email, password });

      if (result.error) {
        return { success: false, error: result.error.message || 'Login failed' };
      }

      if (result.data?.user) {
        setUser({
          user_id: result.data.user.id,
          email: result.data.user.email,
          name: result.data.user.name
        });
        return { success: true };
      }

      return { success: false, error: 'Login failed' };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await authClient.signOut();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
    }
  };

  const signup = async (data: SignupData): Promise<{ success: boolean; error?: string }> => {
    try {
      // Step 1: Create user with FastAPI auth endpoint
      const authResult = await authClient.signUp.email({
        email: data.email,
        password: data.password,
        name: data.email.split('@')[0]
      });

      if (authResult.error) {
        return { success: false, error: authResult.error.message || 'Signup failed' };
      }

      if (!authResult.data?.user) {
        return { success: false, error: 'Signup failed' };
      }

      // Step 2: Store profile in FastAPI backend
      const profileResponse = await fetch(`${FASTAPI_URL}/user/profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          user_id: authResult.data.user.id,
          software_background: data.software_background,
          hardware_background: data.hardware_background
        })
      });

      if (!profileResponse.ok) {
        console.error('Profile creation failed');
      }

      setUser({
        user_id: authResult.data.user.id,
        email: authResult.data.user.email,
        name: authResult.data.user.name
      });

      return { success: true };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: 'Network error. Please try again.' };
    }
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    logout,
    signup,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthProvider;
