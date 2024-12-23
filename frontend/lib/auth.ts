import { jwtDecode } from 'jwt-decode';
import Cookies from 'js-cookie';
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

export interface Session {
  accessToken: string;
  refreshToken: string;
  user: {
    id: string;
    username: string;
    email: string;
    role: 'GUEST' | 'STUDENT' | 'INSTRUCTOR' | 'ADMIN';
  };
  expiresAt: number;
}

export async function getSession(): Promise<Session | null> {
  const accessToken = Cookies.get('accessToken');
  const refreshToken = Cookies.get('refreshToken');

  // For development, return a mock session if no tokens
  if (!accessToken) {
    console.warn('No access token, returning guest session');
    return {
      accessToken: '',
      refreshToken: '',
      user: {
        id: 'guest',
        username: 'Guest',
        email: 'guest@example.com',
        role: 'GUEST'
      },
      expiresAt: Date.now() + 3600 // 1 hour from now
    };
  }

  try {
    const decodedToken = jwtDecode<{
      sub: string;
      exp: number;
      username: string;
      email: string;
      role: 'GUEST' | 'STUDENT' | 'INSTRUCTOR' | 'ADMIN';
    }>(accessToken);

    // Check if token is expired
    if (decodedToken.exp * 1000 < Date.now()) {
      // Attempt to refresh token
      const newSession = await refreshTokens(refreshToken);
      return newSession;
    }

    return {
      accessToken,
      refreshToken: refreshToken || '',
      user: {
        id: decodedToken.sub,
        username: decodedToken.username,
        email: decodedToken.email,
        role: decodedToken.role
      },
      expiresAt: decodedToken.exp
    };
  } catch (error) {
    // Invalid token
    console.warn('Invalid token, returning guest session');
    return {
      accessToken: '',
      refreshToken: '',
      user: {
        id: 'guest',
        username: 'Guest',
        email: 'guest@example.com',
        role: 'GUEST'
      },
      expiresAt: Date.now() + 3600 // 1 hour from now
    };
  }
}

async function refreshTokens(refreshToken?: string): Promise<Session | null> {
  if (!refreshToken) return null;

  try {
    const response = await axios.post(`${API_BASE_URL}/auth/refresh`, { refreshToken });

    const { accessToken, refreshToken: newRefreshToken } = response.data;

    // Store new tokens
    Cookies.set('accessToken', accessToken, { expires: 1/24 }); // 1 hour
    Cookies.set('refreshToken', newRefreshToken, { expires: 7 }); // 7 days

    // Decode and return new session
    const decodedToken = jwtDecode<{
      sub: string;
      exp: number;
      username: string;
      email: string;
      role: 'GUEST' | 'STUDENT' | 'INSTRUCTOR' | 'ADMIN';
    }>(accessToken);

    return {
      accessToken,
      refreshToken: newRefreshToken,
      user: {
        id: decodedToken.sub,
        username: decodedToken.username,
        email: decodedToken.email,
        role: decodedToken.role
      },
      expiresAt: decodedToken.exp
    };
  } catch (error) {
    // Refresh failed, clear tokens
    Cookies.remove('accessToken');
    Cookies.remove('refreshToken');
    return null;
  }
}

export async function login(email: string, password: string) {
  try {
    const response = await axios.post(`${API_BASE_URL}/users/token`, { 
      username: email,  // Backend expects username, not email
      password 
    });

    const { access_token: accessToken } = response.data;

    // Store tokens in cookies
    Cookies.set('accessToken', accessToken, { expires: 1/24 }); // 1 hour

    return await getSession();
  } catch (error) {
    console.error('Login error', error);
    return null;
  }
}

export function logout() {
  Cookies.remove('accessToken');
  Cookies.remove('refreshToken');
  // Optionally, call backend logout endpoint
  window.location.href = '/'; // Redirect to home page
}

export function isAuthenticated(): boolean {
  return !!Cookies.get('accessToken');
}

export function getUserRole() {
  const session = getSession();
  return session?.user.role;
}
