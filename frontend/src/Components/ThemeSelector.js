import React, { useState } from 'react';
import './ThemeSelector.css';

const ThemeSelector = () => {
  const [selectedTheme, setSelectedTheme] = useState(null);

  const themes = [
    { name: 'Bakery', description: 'Warm & inviting design for culinary creators', imgSrc: 'https://images.unsplash.com/photo-1517433670267-08bbd4be890f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', value: 'bakery' },
    { name: 'Tech', description: 'Modern & sleek design for innovators', imgSrc: 'https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', value: 'tech' },
    { name: 'Fashion', description: 'Elegant & stylish design for trendsetters', imgSrc: 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', value: 'fashion' },
    { name: 'Wellness', description: 'Calming & peaceful design for health professionals', imgSrc: 'https://images.unsplash.com/photo-1545205597-3d9d02c29597?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', value: 'wellness' },
    { name: 'Minimalist', description: 'Clean & simple design for focused work', imgSrc: 'https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', value: 'minimalist' },
    { name: 'Creative', description: 'Vibrant & artistic design for creative professionals', imgSrc: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80', value: 'creative' }
  ];

  const handleThemeSelect = (theme) => {
    setSelectedTheme(theme);
  };

  return (
    <div className="theme-container">
      <div className="theme-header">
        <h1>Choose Your Theme</h1>
        <p>Select a theme that matches your brand's personality</p>
      </div>
      <div className="theme-grid">
        {themes.map((theme, index) => (
          <div
            key={index}
            className={`theme-option ${selectedTheme === theme.value ? 'selected' : ''}`}
            data-theme={theme.value}
            onClick={() => handleThemeSelect(theme.value)}
          >
            <img src={theme.imgSrc} alt={`${theme.name} Theme`} />
            <div className="theme-overlay">
              <h3 className="theme-name">{theme.name}</h3>
              <p className="theme-description">{theme.description}</p>
            </div>
          </div>
        ))}
        <a href="index.html" className="general-theme">
          <i className="fas fa-palette"></i>
          <span>Use General Theme</span>
        </a>
      </div>
    </div>
  );
};

export default ThemeSelector;
