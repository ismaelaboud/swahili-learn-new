import axios from 'axios';
import { z } from 'zod';
import { getSession } from '../auth';

// User Schema
export const userSchema = z.object({
  id: z.string(),
  username: z.string(),
  email: z.string().email(),
  role: z.enum(['STUDENT', 'INSTRUCTOR', 'ADMIN']),
  profilePicture: z.string().optional(),
  bio: z.string().optional()
});

// Create an axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
  withCredentials: true,
});

// Interceptor to add authentication token
api.interceptors.request.use(async (config) => {
  try {
    const session = await getSession();
    if (session?.accessToken) {
      config.headers['Authorization'] = `Bearer ${session.accessToken}`;
    }
    return config;
  } catch (error) {
    console.error('Error in request interceptor:', error);
    return config;
  }
});

// Types
export type User = z.infer<typeof userSchema>;

// Registration function
export async function registerUser(userData: {
  username: string;
  email: string;
  password: string;
  role: 'STUDENT' | 'INSTRUCTOR';
}) {
  try {
    const response = await api.post('/auth/register', userData);
    return userSchema.parse(response.data);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Handle specific error responses from the backend
      if (error.response) {
        switch (error.response.status) {
          case 400:
            throw new Error('Invalid registration data');
          case 409:
            throw new Error('User already exists');
          default:
            throw new Error('Registration failed');
        }
      } else if (error.request) {
        // No response received
        throw new Error('No response from server');
      }
    }
    // Generic error
    throw new Error('Registration failed');
  }
}

// Get User Profile
export async function getUserProfile(userId: string) {
  try {
    const response = await api.get(`/users/${userId}`);
    return userSchema.parse(response.data);
  } catch (error) {
    console.error('Failed to fetch user profile', error);
    throw error;
  }
}

// Update User Profile
export async function updateUserProfile(userId: string, profileData: Partial<User>) {
  try {
    const response = await api.patch(`/users/${userId}`, profileData);
    return userSchema.parse(response.data);
  } catch (error) {
    console.error('Profile update failed', error);
    throw error;
  }
}

// List Users (for admin)
export async function listUsers(params?: {
  page?: number;
  pageSize?: number;
  role?: string;
}) {
  try {
    const response = await api.get('/users', { params });
    return {
      users: z.array(userSchema).parse(response.data.users),
      total: response.data.total,
      page: response.data.page,
      pageSize: response.data.pageSize
    };
  } catch (error) {
    console.error('Failed to list users', error);
    throw error;
  }
}

// Delete User (for admin)
export async function deleteUser(userId: string) {
  try {
    const response = await api.delete(`/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to delete user', error);
    throw error;
  }
}
