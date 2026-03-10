import React, { useState } from 'react';

function OnboardingWizard() {
  const [role, setRole] = useState('');

  return (
    <div>
      <h1>Welcome to HuhlyHub</h1>
      <p>I am a:</p>
      <label>
        <input
          type="radio"
          name="role"
          value="musician"
          checked={role === 'musician'}
          onChange={(e) => setRole(e.target.value)}
        />
        Musician
      </label>
      <label>
        <input
          type="radio"
          name="role"
          value="writer"
          checked={role === 'writer'}
          onChange={(e) => setRole(e.target.value)}
        />
        Writer
      </label>
      <label>
        <input
          type="radio"
          name="role"
          value="video-creator"
          checked={role === 'video-creator'}
          onChange={(e) => setRole(e.target.value)}
        />
        Video Creator
      </label>
      <button>Get Started</button>
    </div>
  );
}

export default OnboardingWizard;
