import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../MainPage.css'; // optional: import your CSS for styling

export default function MainPage() {
  const navigate = useNavigate();

  return (
    <div className="main-page">
      {/* Header / Top Panel */}
      <header className="main-header">
        <div className="logo"></div>
        {/* The button can be styled to have different hues/panels */}
        <button 
          className="nav-button"
          onClick={() => navigate('/models')}
        >
          Go to Models
        </button>
      </header>

      {/* Main content: information, project images, etc. */}
      <section className="info-section">
        <h1>Personal Gym Visualizer ?</h1>
        <p>
          Here you can find information about our gym workout models and try them out yourself!
        </p>
      </section>
    </div>
  );
}
