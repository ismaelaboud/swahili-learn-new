import axios from 'axios';
import { getSession } from '../auth'; // We'll create this later

// Create an axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
  withCredentials: true,
});

// Interceptor to add authentication token
api.interceptors.request.use(async (config) => {
  try {
    const session = await getSession();
    console.log('Session retrieved:', session ? 'Valid' : 'No session');
    
    if (session?.accessToken) {
      console.log('Adding authorization header');
      config.headers['Authorization'] = `Bearer ${session.accessToken}`;
    } else {
      console.warn('No access token available');
    }
    return config;
  } catch (error) {
    console.error('Error in request interceptor:', error);
    return config;
  }
}, (error) => {
  console.error('Interceptor request error:', error);
  return Promise.reject(error);
});

export interface Course {
  id: string;
  title: string;
  description: string;
  instructor: string;
  category: string;
  difficulty: string;
  price: number;
  averageRating: number;
  totalEnrollments: number;
  thumbnailUrl?: string;
}

export interface CourseSearchParams {
  query?: string;
  category?: string;
  difficulty?: string;
  minPrice?: number;
  maxPrice?: number;
  page?: number;
  pageSize?: number;
  sortBy?: 'price' | 'rating' | 'enrollments';
  sortOrder?: 'asc' | 'desc';
}

export async function fetchCourses(params: CourseSearchParams = {}) {
  try {
    console.log('Fetching courses with params:', params);
    console.log('Base URL:', api.defaults.baseURL);
    const response = await api.get('/courses', { params });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch courses', error);
    if (axios.isAxiosError(error)) {
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        headers: error.response?.headers
      });
    }
    throw error;
  }
}

export async function searchCourses(query: string) {
  try {
    const response = await api.get('/courses/search', { params: { query } });
    return response.data;
  } catch (error) {
    console.error('Failed to search courses', error);
    throw error;
  }
}

export async function getCourseDetails(courseId: string) {
  try {
    const response = await api.get(`/courses/${courseId}`);
    return response.data;
  } catch (error) {
    console.error(`Failed to fetch course details for ${courseId}`, error);
    throw error;
  }
}

export async function enrollInCourse(courseId: string) {
  try {
    const response = await api.post(`/courses/${courseId}/enroll`);
    return response.data;
  } catch (error) {
    console.error(`Failed to enroll in course ${courseId}`, error);
    throw error;
  }
}

export async function createCourse(courseData: Partial<Course>) {
  try {
    const response = await api.post('/courses', courseData);
    return response.data;
  } catch (error) {
    console.error('Failed to create course', error);
    throw error;
  }
}

export async function updateCourse(courseId: string, courseData: Partial<Course>) {
  try {
    const response = await api.put(`/courses/${courseId}`, courseData);
    return response.data;
  } catch (error) {
    console.error(`Failed to update course ${courseId}`, error);
    throw error;
  }
}

export async function deleteCourse(courseId: string) {
  try {
    const response = await api.delete(`/courses/${courseId}`);
    return response.data;
  } catch (error) {
    console.error(`Failed to delete course ${courseId}`, error);
    throw error;
  }
}
