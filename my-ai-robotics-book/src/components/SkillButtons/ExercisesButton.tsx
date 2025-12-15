import React, { useState } from 'react';
import styles from './SkillButton.module.css';
import { ExercisesButtonProps, SkillResponse, API_BASE_URL } from './types';

export function ExercisesButton({ chapter }: ExercisesButtonProps) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleClick = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/skills/exercises`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chapter }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error ${response.status}`);
      }

      const data: SkillResponse = await response.json();
      setResult(data.result);
    } catch (err) {
      console.error('Error generating exercises:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate exercises');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.skillButtonContainer}>
      <button
        className={`${styles.skillButton} ${loading ? styles.loadingButton : ''}`}
        onClick={handleClick}
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Generate Exercises'}
      </button>

      {result && (
        <div className={styles.resultContainer}>
          <pre className={styles.resultText}>{result}</pre>
        </div>
      )}

      {error && (
        <div className={styles.errorContainer}>
          <p className={styles.errorText}>{error}</p>
        </div>
      )}
    </div>
  );
}

export default ExercisesButton;
