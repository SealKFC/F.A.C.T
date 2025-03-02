import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from "./pages/MainPage";
import ModelsPage from "./pages/ModelsPage";

function App() {
  return (
    <main className="app-container">
      <Router>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/models" element={<ModelsPage />} />
        </Routes>
      </Router>
    </main>
  );
}

export default App;
