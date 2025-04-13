import React, { useState, useEffect } from 'react';
import { auth } from '../firebase';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook
import './AddCollaborators.css';  // Import the CSS file

const AddCollaborators = () => {
  const [adminId, setAdminId] = useState('');
  const [collaborators, setCollaborators] = useState([{ email: '', password: '' }]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate(); // Initialize useNavigate hook

  useEffect(() => {
    const user = auth.currentUser;
    if (user) {
      setAdminId(user.uid);
    } else {
      alert('You must be logged in to add collaborators.');
      navigate('/login');  // Redirect to login page if user isn't logged in
    }
  }, [navigate]);

  const handleChange = (i, field, value) => {
    const updated = [...collaborators];
    updated[i][field] = value;
    setCollaborators(updated);
  };

  const handleAddField = () => {
    const lastCollaborator = collaborators[collaborators.length - 1];
    if (lastCollaborator.email && lastCollaborator.password) {
      setCollaborators([...collaborators, { email: '', password: '' }]);
      setErrorMessage(''); // Clear any previous error message
    } else {
      setErrorMessage('Please fill in the current collaborator fields before adding another.');
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    const created = [];

    for (let collab of collaborators) {
      if (!collab.email || !collab.password) {
        alert('Both email and password are required.');
        setLoading(false);
        return;
      }

      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (!emailPattern.test(collab.email)) {
        alert(`Invalid email format for ${collab.email}`);
        setLoading(false);
        return;
      }

      try {
        const res = await fetch('http://localhost:5000/create-collaborator', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: collab.email, password: collab.password }),
        });

        const data = await res.json();
        if (data.success) {
          created.push({ email: collab.email, uid: data.uid });
        } else {
          alert(`Error for ${collab.email}: ${data.error}`);
        }
      } catch (error) {
        console.error('Error creating collaborator:', error);
        alert(`Error for ${collab.email}: Could not create collaborator.`);
      }
    }

    if (created.length > 0) {
      try {
        await setDoc(doc(db, 'teams', adminId), {
          adminId,
          collaborators: created,
        });
        alert('Collaborators added and saved!');

        // Navigate to the ThemeSelector page instead of static redirect
        navigate("/theme-selector"); // Programmatically navigate to the ThemeSelector page
      } catch (error) {
        console.error('Error adding collaborators to Firestore:', error);
        alert('Error adding collaborators to Firestore.');
      }
    }

    setLoading(false);
  };

  const handleSkip = () => {
    // Handle skip logic here
    navigate("/theme-selector") // Redirect to theme selector page when skipped
  };

  return (
    <div className="auth-container">
      <h1>Add Collaborators</h1>
      
      {collaborators.map((collab, index) => (
        <div key={index} className="collaborator-field">
          <input
            type="email"
            placeholder="Collaborator Email"
            value={collab.email}
            onChange={(e) => handleChange(index, 'email', e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Collaborator Password"
            value={collab.password}
            onChange={(e) => handleChange(index, 'password', e.target.value)}
            required
          />
        </div>
      ))}

      {/* Display error message when trying to add collaborator without filling the previous one */}
      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {/* Add Collaborator button is only enabled when current fields are filled */}
      <button
        className="add-button"
        onClick={handleAddField}
        disabled={!collaborators[collaborators.length - 1].email || !collaborators[collaborators.length - 1].password}
      >
        Add Collaborator
      </button>

      {/* Submit Button */}
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Submitting...' : 'Submit'}
      </button>

      {/* Skip Button */}
      <button className="skip-button" onClick={handleSkip}>
        Skip for Now
      </button>
    </div>
  );
};

export default AddCollaborators;
