/**
 * Authentication client for FastAPI backend
 * Replaces Better Auth with direct FastAPI calls
 */

const AUTH_URL = "https://muniza-nabeel-hackathon.hf.space/api/auth";

interface User {
  id: string;
  email: string;
  name?: string;
  emailVerified?: boolean;
}

interface Session {
  token: string;
  expiresAt?: string;
}

interface AuthResponse {
  user?: User;
  session?: Session;
  error?: { message: string };
}

interface SignUpParams {
  email: string;
  password: string;
  name?: string;
}

interface SignInParams {
  email: string;
  password: string;
}

async function fetchWithCredentials(url: string, options: RequestInit = {}): Promise<Response> {
  return fetch(url, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
}

export const authClient = {
  signUp: {
    email: async (params: SignUpParams): Promise<{ data?: { user: User }; error?: { message: string } }> => {
      try {
        const response = await fetchWithCredentials(`${AUTH_URL}/sign-up/email`, {
          method: 'POST',
          body: JSON.stringify(params),
        });

        const data: AuthResponse = await response.json();

        if (!response.ok || data.error) {
          return { error: { message: data.error?.message || 'Signup failed' } };
        }

        return { data: { user: data.user! } };
      } catch (error) {
        return { error: { message: 'Network error. Please try again.' } };
      }
    },
  },

  signIn: {
    email: async (params: SignInParams): Promise<{ data?: { user: User }; error?: { message: string } }> => {
      try {
        const response = await fetchWithCredentials(`${AUTH_URL}/sign-in/email`, {
          method: 'POST',
          body: JSON.stringify(params),
        });

        const data: AuthResponse = await response.json();

        if (!response.ok || data.error) {
          return { error: { message: data.error?.message || 'Login failed' } };
        }

        return { data: { user: data.user! } };
      } catch (error) {
        return { error: { message: 'Network error. Please try again.' } };
      }
    },
  },

  signOut: async (): Promise<void> => {
    try {
      await fetchWithCredentials(`${AUTH_URL}/sign-out`, {
        method: 'POST',
      });
    } catch (error) {
      console.error('Signout error:', error);
    }
  },

  getSession: async (): Promise<{ data?: { user: User; session: Session } } | null> => {
    try {
      const response = await fetchWithCredentials(`${AUTH_URL}/get-session`, {
        method: 'GET',
      });

      const data: AuthResponse = await response.json();

      if (!data.user || !data.session) {
        return null;
      }

      return { data: { user: data.user, session: data.session } };
    } catch (error) {
      console.error('Get session error:', error);
      return null;
    }
  },
};

// Export for compatibility
export const { signIn, signUp, signOut } = authClient;
