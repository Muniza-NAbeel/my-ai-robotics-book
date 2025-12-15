/**
 * Main Chatbot Component with Skill Buttons and Personalization
 *
 * Features:
 * - Skill buttons: Glossary, Diagram, Translate, Quiz
 * - Quiz MCQ experience with difficulty levels
 * - Personalized greetings for authenticated users
 * - Sends credentials with requests for personalized responses
 */

import React, { useState, useCallback, useRef, useEffect } from 'react';
import styles from './Chatbot.module.css';

// Configure your backend URL here (replace with your deployed backend URL in production)
const API_BASE_URL = 'http://localhost:8000';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  type?: 'normal' | 'correct' | 'incorrect';
}

interface SkillButton {
  label: string;
  icon: string;
  skill: string;
  placeholder: string;
  prompt: string;
}

interface QuizQuestion {
  question: string;
  options: string[];
  correctIndex: number;
}

interface QuizData {
  topic: string;
  questions: {
    easy: QuizQuestion;
    medium: QuizQuestion;
    advanced: QuizQuestion;
  };
}

const SKILL_BUTTONS: SkillButton[] = [
  {
    label: 'Glossary',
    icon: '📘',
    skill: 'glossary',
    placeholder: 'Enter a term to define...',
    prompt: 'Type a term and I will explain its meaning.'
  },
  {
    label: 'Diagram',
    icon: '📊',
    skill: 'diagram',
    placeholder: 'Enter a topic for diagram...',
    prompt: 'Type a topic and I will create an ASCII diagram for it.'
  },
  {
    label: 'Translate',
    icon: '🌐',
    skill: 'translate',
    placeholder: 'Enter English text to translate...',
    prompt: 'Type English text and I will translate it to Urdu.'
  },
  {
    label: 'Quiz',
    icon: '✏️',
    skill: 'exercises',
    placeholder: 'Enter a topic for quiz...',
    prompt: 'Type a topic and I will generate a quiz for you.'
  },
];

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSkillButtons, setShowSkillButtons] = useState(true);
  const [activeSkill, setActiveSkill] = useState<SkillButton | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  // Quiz state
  const [quizData, setQuizData] = useState<QuizData | null>(null);
  const [showDifficultyButtons, setShowDifficultyButtons] = useState(false);
  const [activeQuiz, setActiveQuiz] = useState<QuizQuestion | null>(null);
  const [activeDifficulty, setActiveDifficulty] = useState<string | null>(null);
  const [showMCQOptions, setShowMCQOptions] = useState(false);
  const [selectedOptionIndex, setSelectedOptionIndex] = useState<number | null>(null);
  const [answerRevealed, setAnswerRevealed] = useState(false);

  // Personalization state
  const [personalizedGreeting, setPersonalizedGreeting] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch personalized greeting when chatbot opens
  useEffect(() => {
    if (isOpen && personalizedGreeting === null) {
      fetch(`${API_BASE_URL}/api/chatbot/greeting`, {
        credentials: 'include',
      })
        .then(res => res.json())
        .then(data => {
          setPersonalizedGreeting(data.greeting);
          setIsAuthenticated(data.is_authenticated);
        })
        .catch(err => {
          console.error('Failed to fetch greeting:', err);
          setPersonalizedGreeting("Welcome! I'm here to help you learn about AI and Robotics.");
        });
    }
  }, [isOpen, personalizedGreeting]);

  // Focus input when skill is selected
  useEffect(() => {
    if (activeSkill && inputRef.current) {
      inputRef.current.focus();
    }
  }, [activeSkill]);

  const toggleChat = useCallback(() => {
    setIsOpen((prev) => !prev);
  }, []);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setInputMessage(e.target.value);
    },
    []
  );

  // Handle MCQ option click
  const handleOptionClick = useCallback((optionIndex: number) => {
    if (!activeQuiz || answerRevealed) return;

    setSelectedOptionIndex(optionIndex);
    setAnswerRevealed(true);

    const isCorrect = optionIndex === activeQuiz.correctIndex;
    const correctOption = activeQuiz.options[activeQuiz.correctIndex];

    // Add feedback message
    const feedbackMessage: Message = {
      id: Date.now(),
      text: isCorrect
        ? `✅ Correct! "${correctOption}" is the right answer.`
        : `❌ Wrong! The correct answer is: "${correctOption}"`,
      sender: 'bot',
      type: isCorrect ? 'correct' : 'incorrect',
    };
    setMessages((prev) => [...prev, feedbackMessage]);

    // After a short delay, show option to continue
    setTimeout(() => {
      setShowMCQOptions(false);
      setActiveQuiz(null);
      setActiveDifficulty(null);
      setSelectedOptionIndex(null);
      setAnswerRevealed(false);

      if (quizData) {
        setShowDifficultyButtons(true);
        const nextMessage: Message = {
          id: Date.now() + 1,
          text: 'Select another difficulty level or click × to exit quiz.',
          sender: 'bot',
        };
        setMessages((prev) => [...prev, nextMessage]);
      }
    }, 1500);
  }, [activeQuiz, answerRevealed, quizData]);

  const sendMessage = useCallback(
    async (query: string, skill: string | null = null) => {
      if (!query.trim()) return;

      const userMessage: Message = {
        id: Date.now(),
        text: query,
        sender: 'user',
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputMessage('');

      setIsLoading(true);

      // Hide skill buttons after first interaction
      if (showSkillButtons) {
        setShowSkillButtons(false);
      }

      try {
        // Include credentials for personalization
        const response = await fetch(`${API_BASE_URL}/api/chatbot`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',  // Send cookies for auth
          body: JSON.stringify({
            query,
            skill,
          }),
        });

        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const data = await response.json();

        // Handle quiz response
        if (skill === 'exercises' && data.type === 'quiz') {
          try {
            const quiz: QuizData = JSON.parse(data.response);
            setQuizData(quiz);
            setShowDifficultyButtons(true);

            const botMessage: Message = {
              id: Date.now() + 1,
              text: `📝 Quiz ready for "${quiz.topic}"\n\nSelect a difficulty level:`,
              sender: 'bot',
            };
            setMessages((prev) => [...prev, botMessage]);
          } catch {
            // Fallback for non-JSON response
            const botMessage: Message = {
              id: Date.now() + 1,
              text: data.response,
              sender: 'bot',
            };
            setMessages((prev) => [...prev, botMessage]);
          }
        } else {
          const botMessage: Message = {
            id: Date.now() + 1,
            text: data.response,
            sender: 'bot',
          };
          setMessages((prev) => [...prev, botMessage]);
        }
      } catch (error) {
        console.error('Error sending:', error);

        const errorMessage: Message = {
          id: Date.now() + 1,
          text: 'Connection error. Please check your network and try again.',
          sender: 'bot',
        };

        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [showSkillButtons]
  );

  const handleDifficultySelect = useCallback((difficulty: 'easy' | 'medium' | 'advanced') => {
    if (!quizData) return;

    const question = quizData.questions[difficulty];
    setActiveQuiz(question);
    setActiveDifficulty(difficulty);
    setShowDifficultyButtons(false);
    setShowMCQOptions(true);
    setSelectedOptionIndex(null);
    setAnswerRevealed(false);

    const difficultyEmoji = difficulty === 'easy' ? '📗' : difficulty === 'medium' ? '📙' : '📕';
    const difficultyLabel = difficulty.charAt(0).toUpperCase() + difficulty.slice(1);

    const questionMessage: Message = {
      id: Date.now(),
      text: `${difficultyEmoji} ${difficultyLabel} Question:\n\n${question.question}`,
      sender: 'bot',
    };
    setMessages((prev) => [...prev, questionMessage]);
  }, [quizData]);

  const handleSkillClick = useCallback(
    (skill: SkillButton) => {
      // Set active skill and show prompt message
      setActiveSkill(skill);
      setShowSkillButtons(false);

      // Add bot message prompting for input
      const promptMessage: Message = {
        id: Date.now(),
        text: `${skill.icon} ${skill.prompt}`,
        sender: 'bot',
      };
      setMessages((prev) => [...prev, promptMessage]);
    },
    []
  );

  const handleKeyPress = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !isLoading && inputMessage.trim()) {
        // Send with active skill if one is selected
        sendMessage(inputMessage, activeSkill?.skill || null);
      }
    },
    [inputMessage, isLoading, sendMessage, activeSkill]
  );

  const handleSendClick = useCallback(() => {
    if (inputMessage.trim()) {
      // Send with active skill if one is selected
      sendMessage(inputMessage, activeSkill?.skill || null);
    }
  }, [inputMessage, sendMessage, activeSkill]);

  const handleCancelSkill = useCallback(() => {
    setActiveSkill(null);
    setShowSkillButtons(true);
    setMessages([]);
    // Reset quiz state
    setQuizData(null);
    setShowDifficultyButtons(false);
    setActiveQuiz(null);
    setActiveDifficulty(null);
    setShowMCQOptions(false);
    setSelectedOptionIndex(null);
    setAnswerRevealed(false);
  }, []);

  // Get placeholder text based on active skill
  const getPlaceholder = () => {
    if (activeSkill) {
      return activeSkill.placeholder;
    }
    return 'Ask a question about the book...';
  };

  // Get message style class
  const getMessageClass = (msg: Message) => {
    let classes = `${styles.message} ${styles[msg.sender]}`;
    if (msg.type === 'correct') {
      classes += ` ${styles.correct}`;
    } else if (msg.type === 'incorrect') {
      classes += ` ${styles.incorrect}`;
    }
    return classes;
  };

  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.chatIcon} onClick={toggleChat}>
        💬
      </button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>
              {activeSkill ? `${activeSkill.icon} ${activeSkill.label}` : 'AI Assistant'}
            </h3>
            <button onClick={toggleChat} className={styles.closeButton}>
              ×
            </button>
          </div>

          <div className={styles.chatMessages}>
            {/* Personalized greeting shown at start */}
            {showSkillButtons && messages.length === 0 && personalizedGreeting && (
              <div className={`${styles.message} ${styles.bot}`}>
                {personalizedGreeting}
                {!isAuthenticated && (
                  <div style={{ marginTop: '8px', fontSize: '12px', opacity: 0.8 }}>
                    <a href="/signup" style={{ color: '#007bff' }}>Sign up</a> for personalized learning!
                  </div>
                )}
              </div>
            )}

            {/* Skill buttons shown only at start */}
            {showSkillButtons && messages.length === 0 && (
              <div className={styles.skillButtonsContainer}>
                {SKILL_BUTTONS.map((skill) => (
                  <button
                    key={skill.skill}
                    className={styles.skillButton}
                    onClick={() => handleSkillClick(skill)}
                    disabled={isLoading}
                  >
                    <span className={styles.skillIcon}>{skill.icon}</span>
                    <span className={styles.skillLabel}>{skill.label}</span>
                  </button>
                ))}
              </div>
            )}

            {/* Chat messages */}
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={getMessageClass(msg)}
              >
                {msg.text}
              </div>
            ))}

            {/* Difficulty buttons for quiz */}
            {showDifficultyButtons && quizData && (
              <div className={styles.difficultyButtonsContainer}>
                <button
                  className={`${styles.difficultyButton} ${styles.easy}`}
                  onClick={() => handleDifficultySelect('easy')}
                >
                  📗 Easy
                </button>
                <button
                  className={`${styles.difficultyButton} ${styles.medium}`}
                  onClick={() => handleDifficultySelect('medium')}
                >
                  📙 Medium
                </button>
                <button
                  className={`${styles.difficultyButton} ${styles.advanced}`}
                  onClick={() => handleDifficultySelect('advanced')}
                >
                  📕 Advanced
                </button>
              </div>
            )}

            {/* MCQ Options */}
            {showMCQOptions && activeQuiz && (
              <div className={styles.mcqOptionsContainer}>
                {activeQuiz.options.map((option, index) => {
                  let optionClass = styles.mcqOption;
                  if (answerRevealed) {
                    if (index === activeQuiz.correctIndex) {
                      optionClass += ` ${styles.correctOption}`;
                    } else if (index === selectedOptionIndex) {
                      optionClass += ` ${styles.wrongOption}`;
                    } else {
                      optionClass += ` ${styles.disabledOption}`;
                    }
                  }
                  return (
                    <button
                      key={index}
                      className={optionClass}
                      onClick={() => handleOptionClick(index)}
                      disabled={answerRevealed}
                    >
                      <span className={styles.optionLetter}>
                        {String.fromCharCode(65 + index)}
                      </span>
                      <span className={styles.optionText}>{option}</span>
                    </button>
                  );
                })}
              </div>
            )}

            {/* Loading indicator */}
            {isLoading && (
              <div className={`${styles.message} ${styles.bot}`}>
                Thinking...
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputContainer}>
            {/* Active skill indicator */}
            {activeSkill && (
              <button
                className={styles.skillTag}
                onClick={handleCancelSkill}
                title="Click to cancel"
              >
                {activeSkill.icon} ×
              </button>
            )}

            <input
              ref={inputRef}
              type="text"
              className={styles.chatInput}
              placeholder={getPlaceholder()}
              value={inputMessage}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              disabled={isLoading || showDifficultyButtons || showMCQOptions}
            />

            <button
              onClick={handleSendClick}
              className={styles.sendButton}
              disabled={isLoading || !inputMessage.trim() || showDifficultyButtons || showMCQOptions}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
