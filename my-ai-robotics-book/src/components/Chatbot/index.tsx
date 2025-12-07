import React, { useState, useCallback, useRef, useEffect } from 'react';
import styles from './Chatbot.module.css';

const API_BASE_URL = (typeof process !== 'undefined' ? process.env.NEXT_PUBLIC_API_URL : undefined) || "http://localhost:8000";

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = useCallback(() => {
    setIsOpen(prev => !prev);
  }, []);

  const handleInputChange = useCallback((e) => {
    setInputMessage(e.target.value);
  }, []);

  const getSelectedText = () => {
    if (typeof window !== 'undefined' && window.getSelection) {
      return window.getSelection().toString();
    }
    return '';
  };

  const sendMessage = useCallback(async (question, selectedText = null) => {
    if (!question.trim() && !selectedText) return;

    const newMessage = { id: messages.length + 1, text: question, sender: 'user', selectedText };
    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, selected_text: selectedText }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      setMessages(prev => [...prev, { id: prev.length + 1, text: data.answer, sender: 'bot' }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        { id: prev.length + 1, text: "Sorry, I couldn't get a response.", sender: 'bot' },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [messages.length]);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter' && !isLoading) sendMessage(inputMessage);
  }, [inputMessage, isLoading, sendMessage]);

  const handleAskWithSelection = useCallback(() => {
    const selectedText = getSelectedText();
    const question = inputMessage.trim();

    if (!question && !selectedText) {
      alert('Please enter a question or select text on the page.');
      return;
    }
    sendMessage(question, selectedText);
  }, [inputMessage, sendMessage]);

  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.chatIcon} onClick={toggleChat}>💬</button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>Book Chatbot</h3>
            <button onClick={toggleChat} className={styles.closeButton}>×</button>
          </div>

          <div className={styles.chatMessages}>
            {messages.map(msg => (
              <div key={msg.id} className={`${styles.message} ${styles[msg.sender]}`}>
                {msg.text}
                {msg.selectedText && <p className={styles.selectedTextContext}>Context: "{msg.selectedText}"</p>}
              </div>
            ))}
            {isLoading && <div className={styles.message}>...typing</div>}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputContainer}>
            <input
              type="text"
              className={styles.chatInput}
              placeholder="Ask a question about the book..."
              value={inputMessage}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
            />
            <button onClick={() => sendMessage(inputMessage)} className={styles.sendButton} disabled={isLoading}>Send</button>
            <button onClick={handleAskWithSelection} className={styles.selectionButton} disabled={isLoading}>Ask with selection</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
