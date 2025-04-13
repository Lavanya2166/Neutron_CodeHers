import React, { useState } from 'react';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../../firebase';
import { useNavigate, Link } from 'react-router-dom';
import './Signup.css';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      return;
    }

    setLoading(true);

    try {
      await createUserWithEmailAndPassword(auth, email, password);
      navigate('/add-collaborators');
    } catch (err) {
      console.error('Error signing up: ', err.message);
      alert('Error signing up: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h1>
  Welcome to <span style={{ 
    color: '#007bff', 
    fontWeight: 'bold', 
    fontStyle: 'italic', 
    fontSize: '1.1em', 
    fontFamily: 'Georgia, serif' 
  }}>PROMPTLY</span>
</h1>

      <h2>Sign Up</h2>
      <form onSubmit={handleSignup}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Signing up...' : 'Sign Up'}
        </button>
      </form>
      <div className="bottom-link">
        Already a member? <Link to="/login">Log in</Link>
      </div>
    </div>
  );
};

export default Signup;
