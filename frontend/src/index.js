import React from 'react';
import ReactDOM from 'react-dom/client';  // Import from react-dom/client
import App from './App';
import './index.css';  // Optional for global styles

// Create a root with the new API
const root = ReactDOM.createRoot(document.getElementById('root'));  

// Render the App inside the StrictMode
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

