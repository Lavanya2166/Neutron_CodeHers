import React, { useState, useEffect } from 'react';
import { auth } from '../firebase';
import { doc, setDoc } from 'firebase/firestore';
import { db } from '../firebase';

const AddCollaborators = () => {
  const [adminId, setAdminId] = useState('');
  const [collaborators, setCollaborators] = useState([{ email: '', password: '' }]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const user = auth.currentUser;
    if (user) {
      setAdminId(user.uid);
    } else {
      alert('You must be logged in to add collaborators.');
      window.location.href = 'login.html'; // use static redirect
    }
  }, []);

  const handleChange = (i, field, value) => {
    const updated = [...collaborators];
    updated[i][field] = value;
    setCollaborators(updated);
  };

  const handleAddField = () => {
    setCollaborators([...collaborators, { email: '', password: '' }]);
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
        window.location.href = 'themes.html'; // redirect to themes.html
      } catch (error) {
        console.error('Error adding collaborators to Firestore:', error);
        alert('Error adding collaborators to Firestore.');
      }
    }

    setLoading(false);
  };

  const handleSkip = () => {
    window.location.href = 'themes.html'; // skip collaborators
  };

  return (
    <div>
      <h2>Add Collaborators</h2>
      {collaborators.map((c, i) => (
        <div key={i}>
          <input
            placeholder="Email"
            value={c.email}
            onChange={(e) => handleChange(i, 'email', e.target.value)}
          />
          <input
            placeholder="Password"
            type="password"
            value={c.password}
            onChange={(e) => handleChange(i, 'password', e.target.value)}
          />
        </div>
      ))}
      <button onClick={handleAddField}>+ Add More</button>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Submitting...' : 'Submit'}
      </button>
      <button onClick={handleSkip} style={{ marginLeft: '10px' }}>
        Skip for now
      </button>
    </div>
  );
};

export default AddCollaborators;
