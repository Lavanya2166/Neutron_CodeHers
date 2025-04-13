// login.js
import React, { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../firebase";
import { useNavigate } from "react-router-dom";
import './Login.css'; // Make sure to import the CSS

const Login = () => {
  const navigate = useNavigate();
  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (event) => {
    event.preventDefault();

    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        const user = userCredential.user;
        console.log("User logged in: ", user);
        navigate("/dashboard");
      })
      .catch((error) => {
        setError(error.message);
        console.error("Login error: ", error.message);
      });
  };

  return (
    <div className="auth-container">
      <h1>Welcome Back</h1>
      <h2>Login to Your Account</h2>
      <form onSubmit={handleLogin}>
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
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit">Login</button>
      </form>
      <div className="bottom-link">
        Don't have an account? <a href="/signup">Sign Up</a>
      </div>
    </div>
  );
};

export default Login;
