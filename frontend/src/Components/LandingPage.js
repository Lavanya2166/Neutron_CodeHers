import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css'; // Make sure this CSS file exists for styling

function LandingPage() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [theme, setTheme] = useState('default');
  const navigate = useNavigate(); // Hook for navigation

  const carouselItems = [
    {
      image: 'https://www.adamenfroy.com/wp-content/uploads/AdobeStock_485691272.jpeg',
      title: 'AI Tools for Everyone',
      description: 'Harness the power of AI for your creative needs.'
    },
    {
      image: 'https://images.bisnis.com/upload/img/pekerjaan_freelance.png',
      title: 'Freelance with AI',
      description: 'Streamline your workflow with AI-powered tools.'
    },
    {
      image: 'https://www.rappler.com/tachyon/2022/12/2022-12-16T095850Z_383355044_RC2JVX91LLGO_RTRMADP_3_PHILIPPINES-ART-BLOOD-scaled.jpg',
      title: 'Create with AI',
      description: 'Unleash your creative potential using AI-based tools.'
    },
    {
      image: 'https://www.careergirls.org/wp-content/uploads/2018/05/FashionDesigner_1920x1080.jpg',
      title: 'Design with AI',
      description: 'AI-assisted tools for designing and creating unique content.'
    },
    {
      image: 'https://tuhoraonline.com/wp-content/uploads/2021/04/freelancer.jpg',
      title: 'Be a Freelancer',
      description: 'Boost your freelance career with AI tools.'
    },
  ];

  // Handle SignUp Click
  const handleSignUpClick = () => {
    navigate('/signup'); // Navigate to the signup page
  };

  // Handle Login Click
  const handleLoginClick = () => {
    navigate('/login'); // Navigate to the login page
  };

  // Next Slide function
  const handleNextSlide = () => {
    setCurrentSlide((prevSlide) => (prevSlide + 1) % carouselItems.length);
  };

  // Handle Theme Change
  const handleThemeChange = (event) => {
    setTheme(event.target.value);
  };

  // Apply theme when theme state changes
  useEffect(() => {
    const root = document.documentElement.style;
    const themeVars = {
      bakery: ['#F1C27D', '#D2691E'],
      tech: ['#4A90E2', '#FF6F61'],
      clothing: ['#C71585', '#FFD700'],
      handmade: ['#8A2BE2', '#FFD700'],
      default: ['#0d6efd', '#ffc107'],
    };

    root.setProperty('--primary-color', themeVars[theme][0]);
    root.setProperty('--accent-color', themeVars[theme][1]);
  }, [theme]);

  useEffect(() => {
    const slideInterval = setInterval(handleNextSlide, 5000);
    return () => clearInterval(slideInterval);
  }, []);

  return (
    <div>
      {/* === NAVIGATION === */}
      <nav className="landing-nav">
        <div className="nav-left">
          <div className="logo">
            <i className="fas fa-brain"></i>
            <span>AI Tools</span>
          </div>
        </div>
        <div className="nav-right">
          <a href="#about" className="nav-link">About</a>

          {/* Theme dropdown */}
          <select id="themeSwitcher" onChange={handleThemeChange} value={theme} className="theme-dropdown">
            <option value="default">Default</option>
            <option value="bakery">Bakery</option>
            <option value="tech">Tech</option>
            <option value="clothing">Clothing</option>
            <option value="handmade">Handmade</option>
          </select>

          {/* Auth buttons */}
          <button className="auth-btn login-btn" onClick={handleLoginClick}>Login</button>
          <button className="auth-btn signup-btn" onClick={handleSignUpClick}>Sign Up</button>
        </div>
      </nav>

      {/* === CAROUSEL === */}
      <div className="carousel">
        {carouselItems.map((item, index) => (
          <div
            className={`carousel-slide ${index === currentSlide ? 'active' : ''}`}
            key={index}
            style={{ backgroundImage: `url(${item.image})` }}
          >
            <div className="carousel-caption">
              <h2>{item.title}</h2>
              <p>{item.description}</p>
            </div>
          </div>
        ))}
      </div>

      {/* === ABOUT SECTION === */}
      <section id="about" className="about">
        <h2>About AI Tools</h2>
        <div className="about-grid">
          <div className="about-item">
            <i className="fas fa-magic"></i>
            <h3>AI-Powered Creation</h3>
            <p>Generate high-quality content, images, and code with state-of-the-art AI models.</p>
          </div>
          <div className="about-item">
            <i className="fas fa-bolt"></i>
            <h3>Lightning Fast</h3>
            <p>Get instant results with our optimized processing pipeline.</p>
          </div>
          <div className="about-item">
            <i className="fas fa-shield-alt"></i>
            <h3>Secure & Private</h3>
            <p>Your data is encrypted and protected with enterprise-grade security.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default LandingPage;
