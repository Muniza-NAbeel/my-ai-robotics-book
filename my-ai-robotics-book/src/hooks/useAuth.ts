/**
 * Re-export useAuth hook from AuthProvider for convenience.
 *
 * Usage:
 * ```typescript
 * import { useAuth } from '@site/src/hooks/useAuth';
 *
 * function MyComponent() {
 *   const { user, isAuthenticated, login, logout, signup } = useAuth();
 *   // ...
 * }
 * ```
 */

export { useAuth } from '../components/Auth/AuthProvider';
