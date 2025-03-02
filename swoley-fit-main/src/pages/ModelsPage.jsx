import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import VideoDisplay from '../components/VideoDisplay';
import '../ModelsPage.css';
import deadliftImage from "../assets/deadliftbar.jpg";

const models = [
  { id: 1, name: "Deadlift Models", thumbnail: deadliftImage, classType: "workout" },
];

export default function ModelsPage() {
  const navigate = useNavigate();
  const [activeModel, setActiveModel] = useState(null);

  const handleModelTest = async (model, variant) => {
    try {
      // Use variant in the URL: '/start_camera/angle' or '/start_camera/landmark'
      const response = await fetch(`http://localhost:5000/start_camera/${variant}`);
      const data = await response.json();
      console.log("Start camera response:", data.status);

      const selectedModel = {
        ...model,
        variant: variant,
        displayName:
          variant === "landmark"
            ? `${model.name} - Landmark`
            : `${model.name} - Angle Calculation`,
      };
      setActiveModel(selectedModel);
    } catch (error) {
      console.error("Error starting camera:", error);
    }
  };

  const closeOverlay = async () => {
    try {
      const response = await fetch('http://localhost:5000/stop_camera');
      const data = await response.json();
      console.log("Stop camera response:", data.status);
    } catch (error) {
      console.error("Error stopping camera:", error);
    }
    setActiveModel(null);
  };

  return (
    <div className="models-page">
      <header className="models-header">
        <button className="back-button" onClick={() => navigate(-1)}>
          &larr; Back to Main
        </button>
        <h2>Select a Model to Test</h2>
      </header>

      <div className="models-grid">
        {models.map((model) => (
          <div key={model.id} className={`model-card ${model.classType}`}>
            <img src={model.thumbnail} alt={model.name} className="model-thumbnail" />
            <div className="button-group">
              <button
                className="model-button"
                onClick={() => handleModelTest(model, "landmark")}
              >
                Landmark
              </button>
            </div>
          </div>
        ))}
      </div>

      {activeModel && (
        <div className="video-overlay">
          <div className="video-overlay-content">
            <button className="close-overlay" onClick={closeOverlay}>
              &times;
            </button>
            <h3>{activeModel.displayName}</h3>
            <VideoDisplay />
          </div>
        </div>
      )}
    </div>
  );
}
