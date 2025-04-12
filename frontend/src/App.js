import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Signup from "./Components/Auth/Signup";
import Login from "./Components/Auth/Login";
import AddCollaborators from "./Components/AddCollaborators";
import Dashboard from "./Components/Dashboard";
import Themes from "./Components/Themes"; // ✅ Import Themes

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/add-collaborators" element={<AddCollaborators />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/themes" element={<Themes />} /> {/* ✅ Updated to "/themes" */}
        <Route path="/" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;



