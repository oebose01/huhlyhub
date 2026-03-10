import { render, screen, fireEvent } from '@testing-library/react';
import Landing from './Landing';

test('renders HuhlyHub headline', () => {
  render(<Landing />);
  const headline = screen.getByText(/huhlyhub/i);
  expect(headline).toBeInTheDocument();
});

test('renders email signup form', () => {
  render(<Landing />);
  const emailInput = screen.getByPlaceholderText(/email/i);
  const submitButton = screen.getByRole('button', { name: /get early access/i });
  expect(emailInput).toBeInTheDocument();
  expect(submitButton).toBeInTheDocument();
});

test('email input value updates on change', () => {
  render(<Landing />);
  const emailInput = screen.getByPlaceholderText(/email/i);
  fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
  expect(emailInput.value).toBe('test@example.com');
});

test('calls onSubmit with email when form is submitted', () => {
  const handleSubmit = vi.fn();
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
  const button = screen.getByRole('button');
  expect(button).toBeDisabled();
  expect(button).toHaveTextContent(/submitting/i);
});

test('shows success message when isSuccess is true', () => {
  render(<Landing isSuccess={true} />);
  
  const successMessage = screen.getByText(/thank you|success/i);
  expect(successMessage).toBeInTheDocument();
  expect(screen.queryByRole('form')).not.toBeInTheDocument();
});

test('shows error message when isError is true', () => {
  render(<Landing isError={true} errorMessage="Something went wrong" />);
  
  const errorMessage = screen.getByText(/something went wrong/i);
  expect(errorMessage).toBeInTheDocument();
  expect(screen.getByRole('form')).toBeInTheDocument();
  expect(screen.getByRole('button')).not.toBeDisabled();
});
