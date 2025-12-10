# API Configuration and Server Setup Guide

This document provides step-by-step instructions for setting up API keys, running the FastAPI server locally, and integrating with the Docusaurus frontend.

## 1. Setting API Keys for Cohere, Qdrant, and OpenAI

### Step 1: Obtain API Keys

1. **Cohere API Key**:
   - Go to https://dashboard.cohere.ai/
   - Sign up or log in to your account
   - Navigate to "API Keys" section
   - Create a new API key and copy it

2. **Qdrant API Key**:
   - Go to https://qdrant.tech/
   - Sign up for Qdrant Cloud or set up a local instance
   - If using Qdrant Cloud, find your API key in the dashboard
   - If using local instance, you can set a custom key or leave it empty for local development

3. **OpenAI API Key**:
   - Go to https://platform.openai.com/
   - Log in to your account
   - Navigate to "API Keys" section
   - Create a new secret key and copy it

### Step 2: Create Environment Configuration File

1. Navigate to the `backend` directory in your project
2. Create a file named `.env` (or copy from `.env.example` if available)
3. Add the following content to the `.env` file:

```
# API Keys
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_HOST=your_qdrant_host_url_here (e.g., https://your-cluster.qdrant.tech)
OPENAI_API_KEY=your_openai_api_key_here

# Application Settings
APP_NAME=RAG Chatbot Backend
DEBUG=false
LOG_LEVEL=INFO

# Qdrant Settings
QDRANT_COLLECTION_NAME=documents

# Embedding Settings
CHUNK_SIZE=1200
CHUNK_OVERLAP=100
```

### Step 3: Verify Configuration

1. Ensure the `.env` file is in the root of the `backend` directory
2. Make sure the `.env` file is listed in `.gitignore` to prevent committing API keys to version control
3. The application will automatically load these environment variables at startup

## 2. Running the FastAPI Server Locally

### Prerequisites

- Python 3.8 or higher installed
- Pip package manager

### Step 1: Install Dependencies

1. Navigate to the `backend` directory
2. Install the required packages:

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Verify Environment Configuration

1. Ensure your `.env` file is properly configured with all required API keys
2. Make sure all API keys are valid and have the necessary permissions

### Step 3: Start the FastAPI Server

You have two options to start the server:

**Option 1: Direct Python execution**
```bash
cd backend
python main.py
```

**Option 2: Using Uvicorn (recommended for development)**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Verify Server is Running

1. Open your web browser and navigate to `http://localhost:8000`
2. You should see a welcome message indicating the server is running
3. API documentation will be available at `http://localhost:8000/docs`

### Additional Development Options

- Use `--reload` flag to automatically restart the server when code changes
- Use `--host 0.0.0.0` to make the server accessible from other devices on the network
- Use `--port [port_number]` to run on a different port if 8000 is occupied

## 3. Integrating with Docusaurus Frontend

### Step 1: Set Up Docusaurus Frontend

1. If you don't have a Docusaurus project yet, create one:
```bash
npx create-docusaurus@latest my-website classic
cd my-website
```

2. If you already have a Docusaurus project, navigate to its directory:
```bash
cd path/to/your/docusaurus/website
```

### Step 2: Configure API Endpoint

1. In your Docusaurus project, locate or create the configuration file (usually `docusaurus.config.js`)
2. Add environment variables for the backend API endpoint:

```javascript
// In docusaurus.config.js or a separate .env file in the Docusaurus project
const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';
```

### Step 3: Create Chat Component

1. Create a React component for the chat interface in `src/components/ChatInterface/`
2. Here's a basic example of how to connect to the backend API:

```jsx
// src/components/ChatInterface/index.js
import React, { useState } from 'react';
import styles from './ChatInterface.module.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`${BACKEND_API_URL}/api/v1/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: 'session-' + Date.now(),
          message: inputValue,
          mode: 'NORMAL',
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages([...newMessages, { role: 'assistant', content: data.response }]);
      } else {
        throw new Error('Failed to get response from backend');
      }
    } catch (error) {
      setMessages([...newMessages, {
        role: 'error',
        content: 'Error: Could not connect to the backend service'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.messages}>
        {messages.map((msg, index) => (
          <div key={index} className={`${styles.message} ${styles[msg.role]}`}>
            {msg.content}
          </div>
        ))}
        {isLoading && (
          <div className={`${styles.message} ${styles.assistant}`}>
            Thinking...
          </div>
        )}
      </div>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask a question about the documentation..."
          className={styles.input}
        />
        <button onClick={sendMessage} disabled={isLoading} className={styles.sendButton}>
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
```

### Step 4: Add CSS Styling

Create `src/components/ChatInterface/ChatInterface.module.css`:

```css
.chatContainer {
  display: flex;
  flex-direction: column;
  height: 500px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.message {
  margin-bottom: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background-color: #007bff;
  color: white;
  margin-left: auto;
}

.message.assistant {
  background-color: #e9ecef;
  color: #333;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
}

.inputContainer {
  display: flex;
  padding: 16px;
  border-top: 1px solid #ddd;
  background-color: white;
}

.input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 8px;
}

.sendButton {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.sendButton:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
```

### Step 5: Integrate Component into Docusaurus Page

1. Import and use the chat component in your desired page:

```jsx
// Example: In src/pages/index.js or any other page
import React from 'react';
import ChatInterface from '../components/ChatInterface';

function Homepage() {
  return (
    <div>
      <header>
        <h1>Welcome to My Documentation</h1>
      </header>
      <main>
        <section>
          <h2>Ask Questions About This Documentation</h2>
          <ChatInterface />
        </section>
      </main>
    </div>
  );
}

export default Homepage;
```

### Step 6: Run the Integrated Application

1. Start the backend server (in one terminal):
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the Docusaurus frontend (in another terminal):
```bash
cd path/to/docusaurus/website
npm run start
```

### Step 7: Testing the Integration

1. Access the Docusaurus frontend at `http://localhost:3000`
2. Use the chat interface to ask questions
3. Verify that requests are properly sent to the backend
4. Confirm that responses from the backend are displayed in the frontend

## Troubleshooting

### Common Issues:

1. **Backend not starting**: Verify all API keys are valid and properly configured in the `.env` file
2. **Frontend can't connect to backend**: Check that both servers are running and the API URL is correctly configured
3. **CORS errors**: The backend should have CORS middleware configured to allow requests from the frontend domain
4. **API key errors**: Ensure API keys have not expired and have the required permissions

### Environment Variables:

Make sure to set the correct environment variables for your deployment:
- For development: `BACKEND_API_URL=http://localhost:8000`
- For production: `BACKEND_API_URL=https://your-backend-domain.com`