import { render, screen } from '@testing-library/react';
import Landing from './Landing';

test('renders HuhlyHub headline', () => {
  render(<Landing />);
  const headline = screen.getByText(/huhlyhub/i);
  expect(headline).toBeInTheDocument();
});

test('calls onSubmit with email when form is submitted', () => {
  const handleSubmit = vi.fn(e => e.preventDefault());
  render(<Landing onSubmit={handleSubmit} />);
  
  const emailInput = screen.getByPlaceholderText(/email/i);
  fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
  
  const form = screen.getByRole('form');
  fireEvent.submit(form);
  
  expect(handleSubmit).toHaveBeenCalledTimes(1);
  expect(handleSubmit).toHaveBeenCalledWith('test@example.com');
});

test('displays loading state on button when isLoading is true', () => {
  render(<Landing isLoading={true} />);
  
  const button = screen.getByRole('button', { name: /get early access/i });
  expect(button).toBeDisabled();
  expect(button).toHaveTextContent(/submitting/i);
});
