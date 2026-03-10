import { useState } from 'react';

const Landing = ({ onSubmit, isLoading = false, isSuccess = false, isError = false, errorMessage = '' }) => {
  const [email, setEmail] = useState('');

  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit && !isLoading && !isSuccess && !isError) {
      onSubmit(email);
    }
  };

  if (isSuccess) {
    return (
      <div>
        <h1>HuhlyHub</h1>
        <p>Thank you for signing up!</p>
      </div>
    );
  }

  return (
    <div>
      <h1>HuhlyHub</h1>
      {isError && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <form onSubmit={handleSubmit} aria-label="Email signup form">
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={handleChange}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Submitting...' : 'Get Early Access'}
        </button>
      </form>
    </div>
  );
};

export default Landing;
