import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email) return;

    setIsLoading(true);
    setIsError(false);
    setErrorMessage('');

    try {
      // Use environment variables for production
      const functionUrl = import.meta.env.VITE_SUPABASE_FUNCTION_URL;
      const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

      const response = await fetch(functionUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${anonKey}`
        },
        body: JSON.stringify({ email })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      setIsSuccess(true);
    } catch (err) {
      setIsError(true);
      setErrorMessage(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">HuhlyHub</h1>
        <p className="text-xl mb-8">Thank you for signing up!</p>
      </div>
    );
  }

  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold mb-4">HuhlyHub</h1>
      <p className="text-xl mb-8">Protect and monetize your content with blockchain</p>

      {/* Email signup form */}
      <form onSubmit={handleSubmit} className="mb-8">
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={handleChange}
          disabled={isLoading}
          className="border p-2 rounded-l-lg"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-blue-600 text-white p-2 rounded-r-lg disabled:bg-blue-300"
        >
          {isLoading ? 'Submitting...' : 'Get Early Access'}
        </button>
      </form>

      {isError && <p className="text-red-500 mb-4">{errorMessage}</p>}

      {/* Existing buttons */}
      <div className="space-x-4">
        <Link to="/register-content" className="bg-blue-500 text-white px-6 py-3 rounded-lg">Register Content</Link>
        <Link to="/verify" className="bg-gray-500 text-white px-6 py-3 rounded-lg">Verify Content</Link>
      </div>

      {/* Sentry test button */}
      <div className="mt-4">
        <button
          onClick={() => { throw new Error("Sentry test error"); }}
          className="bg-red-500 text-white px-6 py-3 rounded-lg"
        >
          Trigger Error (Sentry test)
        </button>
      </div>
    </div>
  );
}
