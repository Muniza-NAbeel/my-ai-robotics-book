// TypeScript types for Skill Button components

// API Response types
export interface SkillResponse {
  result: string;
}

export interface ErrorResponse {
  error: string;
}

// Component Props
export interface GlossaryButtonProps {
  term: string;
}

export interface DiagramButtonProps {
  topic: string;
}

export interface TranslateButtonProps {
  text: string;
}

export interface ExercisesButtonProps {
  chapter: string;
}

// Component State
export interface SkillButtonState {
  loading: boolean;
  result: string | null;
  error: string | null;
}

// API Base URL
export const API_BASE_URL =
  (typeof process !== 'undefined'
    ? process.env.NEXT_PUBLIC_API_URL
    : undefined) || 'http://localhost:8000';
