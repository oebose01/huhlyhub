import { useState } from 'react';

const Landing = ({ onSubmit }) => {
  const [email, setEmail] = useState('');

  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit(email);
    }
  };

  return (
    <div>
      <h1>HuhlyHub</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={handleChange}
        />
        <button type="submit">Get Early Access</button>
      </form>
    </div>
  );
};

export default Landing;
