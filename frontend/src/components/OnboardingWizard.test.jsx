import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import OnboardingWizard from './OnboardingWizard';

describe('OnboardingWizard', () => {
  it('should render a welcome heading and a get started button', () => {
    render(<OnboardingWizard />);
    
    expect(screen.getByRole('heading', { name: /welcome to huhlyhub/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /get started/i })).toBeInTheDocument();
  });

  it('should display role selection options', () => {
    render(<OnboardingWizard />);
    
    expect(screen.getByText(/i am a/i)).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: /musician/i })).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: /writer/i })).toBeInTheDocument();
    expect(screen.getByRole('radio', { name: /video creator/i })).toBeInTheDocument();
  });
});



