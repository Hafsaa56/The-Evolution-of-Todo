// Basic frontend tests to verify components render
import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../app/page';
import Login from '../app/login/page';
import Register from '../app/register/page';

// Mock the next/navigation module
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    prefetch: jest.fn(),
  }),
  usePathname: jest.fn(),
  useSearchParams: jest.fn(),
}));

// Mock the AuthContext
jest.mock('../context/AuthContext', () => ({
  useAuth: () => ({
    user: null,
    loading: false,
    login: jest.fn(),
    logout: jest.fn(),
    register: jest.fn(),
  }),
}));

describe('Pages', () => {
  it('renders the home page', () => {
    render(<Home />);
    expect(screen.getByText('Welcome to Todo App')).toBeInTheDocument();
    expect(screen.getByText('Sign in')).toBeInTheDocument();
    expect(screen.getByText('Create account')).toBeInTheDocument();
  });

  it('renders the login page', () => {
    render(<Login />);
    expect(screen.getByText('Sign in to your account')).toBeInTheDocument();
    expect(screen.getByLabelText('Email address')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
  });

  it('renders the register page', () => {
    render(<Register />);
    expect(screen.getByText('Create a new account')).toBeInTheDocument();
    expect(screen.getByLabelText('Email address')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByLabelText('Confirm Password')).toBeInTheDocument();
  });
});