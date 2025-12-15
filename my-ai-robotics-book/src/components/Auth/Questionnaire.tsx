import React from 'react';
import styles from './Auth.module.css';

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

interface QuestionnaireProps {
  softwareBackground: SoftwareBackground;
  hardwareBackground: HardwareBackground;
  onSoftwareChange: (data: SoftwareBackground) => void;
  onHardwareChange: (data: HardwareBackground) => void;
  errors?: { [key: string]: string };
}

const PROGRAMMING_LANGUAGES = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'c_cpp', label: 'C/C++' },
  { value: 'none', label: 'None' },
];

const HARDWARE_OPTIONS = [
  { value: 'laptop_only', label: 'Laptop Only' },
  { value: 'raspberry_pi', label: 'Raspberry Pi' },
  { value: 'arduino', label: 'Arduino' },
  { value: 'robotics_kits', label: 'Robotics Kits' },
  { value: 'none', label: 'None' },
];

export function Questionnaire({
  softwareBackground,
  hardwareBackground,
  onSoftwareChange,
  onHardwareChange,
  errors = {},
}: QuestionnaireProps) {
  const handleLanguageToggle = (language: string) => {
    const current = softwareBackground.languages_known;
    const updated = current.includes(language)
      ? current.filter((l) => l !== language)
      : [...current, language];
    onSoftwareChange({ ...softwareBackground, languages_known: updated });
  };

  const handleHardwareToggle = (hardware: string) => {
    const current = hardwareBackground.hardware_access;
    const updated = current.includes(hardware)
      ? current.filter((h) => h !== hardware)
      : [...current, hardware];
    onHardwareChange({ ...hardwareBackground, hardware_access: updated });
  };

  return (
    <div className={styles.questionnaire}>
      {/* Software Background Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>Software Background</h3>

        <div className={styles.field}>
          <label className={styles.label}>Programming Level *</label>
          <select
            className={styles.select}
            value={softwareBackground.programming_level}
            onChange={(e) =>
              onSoftwareChange({
                ...softwareBackground,
                programming_level: e.target.value as SoftwareBackground['programming_level'],
              })
            }
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          {errors.programming_level && (
            <span className={styles.error}>{errors.programming_level}</span>
          )}
        </div>

        <div className={styles.field}>
          <label className={styles.label}>Programming Languages Known *</label>
          <div className={styles.checkboxGroup}>
            {PROGRAMMING_LANGUAGES.map((lang) => (
              <label key={lang.value} className={styles.checkbox}>
                <input
                  type="checkbox"
                  checked={softwareBackground.languages_known.includes(lang.value)}
                  onChange={() => handleLanguageToggle(lang.value)}
                />
                <span>{lang.label}</span>
              </label>
            ))}
          </div>
          {errors.languages_known && (
            <span className={styles.error}>{errors.languages_known}</span>
          )}
        </div>

        <div className={styles.field}>
          <label className={styles.label}>AI/ML Experience *</label>
          <select
            className={styles.select}
            value={softwareBackground.ai_experience}
            onChange={(e) =>
              onSoftwareChange({
                ...softwareBackground,
                ai_experience: e.target.value as SoftwareBackground['ai_experience'],
              })
            }
          >
            <option value="none">None</option>
            <option value="basic">Basic</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>

        <div className={styles.field}>
          <label className={styles.label}>Web Development Experience *</label>
          <select
            className={styles.select}
            value={softwareBackground.web_dev_experience}
            onChange={(e) =>
              onSoftwareChange({
                ...softwareBackground,
                web_dev_experience: e.target.value as SoftwareBackground['web_dev_experience'],
              })
            }
          >
            <option value="none">None</option>
            <option value="basic">Basic</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>

      {/* Hardware Background Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>Hardware / Robotics Background</h3>

        <div className={styles.field}>
          <label className={styles.label}>Do you have robotics experience? *</label>
          <div className={styles.radioGroup}>
            <label className={styles.radio}>
              <input
                type="radio"
                name="robotics_experience"
                checked={hardwareBackground.robotics_experience === true}
                onChange={() =>
                  onHardwareChange({ ...hardwareBackground, robotics_experience: true })
                }
              />
              <span>Yes</span>
            </label>
            <label className={styles.radio}>
              <input
                type="radio"
                name="robotics_experience"
                checked={hardwareBackground.robotics_experience === false}
                onChange={() =>
                  onHardwareChange({ ...hardwareBackground, robotics_experience: false })
                }
              />
              <span>No</span>
            </label>
          </div>
        </div>

        <div className={styles.field}>
          <label className={styles.label}>Electronics Familiarity *</label>
          <select
            className={styles.select}
            value={hardwareBackground.electronics_familiarity}
            onChange={(e) =>
              onHardwareChange({
                ...hardwareBackground,
                electronics_familiarity: e.target.value as HardwareBackground['electronics_familiarity'],
              })
            }
          >
            <option value="none">None</option>
            <option value="basic">Basic</option>
            <option value="intermediate">Intermediate</option>
          </select>
        </div>

        <div className={styles.field}>
          <label className={styles.label}>Hardware Access *</label>
          <div className={styles.checkboxGroup}>
            {HARDWARE_OPTIONS.map((hw) => (
              <label key={hw.value} className={styles.checkbox}>
                <input
                  type="checkbox"
                  checked={hardwareBackground.hardware_access.includes(hw.value)}
                  onChange={() => handleHardwareToggle(hw.value)}
                />
                <span>{hw.label}</span>
              </label>
            ))}
          </div>
          {errors.hardware_access && (
            <span className={styles.error}>{errors.hardware_access}</span>
          )}
        </div>
      </div>
    </div>
  );
}

export default Questionnaire;
