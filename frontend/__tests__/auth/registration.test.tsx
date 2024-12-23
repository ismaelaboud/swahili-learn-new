import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import RegisterPage from '@/app/auth/register/page';
import { registerUser } from '@/lib/api/users';
import { act } from 'react-dom/test-utils';

// Mock the registerUser function
jest.mock('@/lib/api/users', () => ({
  registerUser: jest.fn()
}));

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn()
    };
  }
}));

describe('Registration Page', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it('renders registration form correctly', () => {
    render(<RegisterPage />);
    
    // Check if all form elements are present
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByText('Register')).toBeInTheDocument();
  });

  it('validates input fields', async () => {
    render(<RegisterPage />);
    
    // Try to submit with invalid data
    await act(async () => {
      fireEvent.click(screen.getByText('Register'));
    });

    // Check for validation errors
    expect(screen.getByText('Username must be at least 3 characters')).toBeInTheDocument();
    expect(screen.getByText('Invalid email address')).toBeInTheDocument();
    expect(screen.getByText('Password must be at least 8 characters')).toBeInTheDocument();
  });

  it('successfully registers a user', async () => {
    // Mock successful registration
    (registerUser as jest.Mock).mockResolvedValue({
      id: '123',
      username: 'testuser',
      email: 'test@example.com'
    });

    render(<RegisterPage />);
    
    // Fill out the form
    await act(async () => {
      fireEvent.change(screen.getByPlaceholderText('Username'), { 
        target: { value: 'testuser' } 
      });
      fireEvent.change(screen.getByPlaceholderText('Email'), { 
        target: { value: 'test@example.com' } 
      });
      fireEvent.change(screen.getByPlaceholderText('Password'), { 
        target: { value: 'password123' } 
      });
      
      // Select role
      const roleSelect = screen.getByText('Select Role');
      fireEvent.click(roleSelect);
      const studentOption = screen.getByText('Student');
      fireEvent.click(studentOption);

      // Submit the form
      fireEvent.click(screen.getByText('Register'));
    });

    // Wait for registration to complete
    await waitFor(() => {
      expect(registerUser).toHaveBeenCalledWith({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
        role: 'STUDENT'
      });
    });
  });

  it('handles registration error', async () => {
    // Mock registration error
    (registerUser as jest.Mock).mockRejectedValue(new Error('Registration failed'));

    render(<RegisterPage />);
    
    // Fill out the form
    await act(async () => {
      fireEvent.change(screen.getByPlaceholderText('Username'), { 
        target: { value: 'testuser' } 
      });
      fireEvent.change(screen.getByPlaceholderText('Email'), { 
        target: { value: 'test@example.com' } 
      });
      fireEvent.change(screen.getByPlaceholderText('Password'), { 
        target: { value: 'password123' } 
      });
      
      // Select role
      const roleSelect = screen.getByText('Select Role');
      fireEvent.click(roleSelect);
      const studentOption = screen.getByText('Student');
      fireEvent.click(studentOption);

      // Submit the form
      fireEvent.click(screen.getByText('Register'));
    });

    // Wait for error handling
    await waitFor(() => {
      expect(screen.getByText('An unexpected error occurred')).toBeInTheDocument();
    });
  });
});
