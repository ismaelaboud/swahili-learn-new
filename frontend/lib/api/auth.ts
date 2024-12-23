import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// Send Password Reset Email
export async function sendPasswordResetEmail(email: string) {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/reset-password`, { email });
    return response.data;
  } catch (error) {
    console.error('Password reset email failed', error);
    throw error;
  }
}

// Reset Password
export async function resetPassword(
  email: string, 
  resetToken: string, 
  newPassword: string
) {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/reset-password/confirm`, {
      email,
      resetToken,
      newPassword
    });
    return response.data;
  } catch (error) {
    console.error('Password reset failed', error);
    throw error;
  }
}

// Verify Reset Token
export async function verifyResetToken(email: string, resetToken: string) {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/reset-password/verify`, {
      email,
      resetToken
    });
    return response.data;
  } catch (error) {
    console.error('Reset token verification failed', error);
    throw error;
  }
}

// Change Password (when logged in)
export async function changePassword(
  currentPassword: string, 
  newPassword: string
) {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/change-password`, {
      currentPassword,
      newPassword
    });
    return response.data;
  } catch (error) {
    console.error('Password change failed', error);
    throw error;
  }
}
