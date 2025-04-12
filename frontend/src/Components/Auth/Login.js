// login.js
import React, { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../../firebase";  // Firebase configuration file
import { useNavigate } from "react-router-dom";  // To navigate after successful login

const Login = () => {
  const navigate = useNavigate();
  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (event) => {
    event.preventDefault();

    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        // Successfully logged in
        const user = userCredential.user;
        console.log("User logged in: ", user);
        navigate("/dashboard");  // Redirect to dashboard after login
      })
      .catch((error) => {
        // Handle login errors
        const errorMessage = error.message;
        setError(errorMessage);
        console.error("Login error: ", errorMessage);
      });
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p>{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
