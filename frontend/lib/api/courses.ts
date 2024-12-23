import axios from 'axios';
import { getSession } from '../auth'; // We'll create this later

// Create an axios instance with base configuration
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true,
});

// Interceptor to add authentication token
api.interceptors.request.use(async (config) => {
  try {
    const session = await getSession();
    console.log('Session retrieved:', session ? 'Valid' : 'Invalid');
    
    if (session?.accessToken) {
      console.log('Adding authorization header');
      config.headers['Authorization'] = `Bearer ${session.accessToken}`;
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
  description?: string;
  instructor?: string;
  difficulty?: string;
  categories: string[];
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

export interface CourseResponse {
  courses: Course[];
  total_count: number;
  total_pages: number;
  current_page: number;
}

export async function fetchCourses(params: CourseSearchParams = {}): Promise<CourseResponse> {
  try {
    const response = await api.get('/courses', { 
      params: {
        category: params.category || '',
        difficulty: params.difficulty || '',
        page: params.page || 1,
        pageSize: params.pageSize || 9,
        query: params.query || ''
      }
    });

    return {
      courses: response.data.courses || [],
      total_count: response.data.total_count || 0,
      total_pages: response.data.total_pages || 1,
      current_page: response.data.current_page || 1
    };
  } catch (error) {
    console.error('Failed to fetch courses', error);
    
    // Mock courses with free images from Unsplash
    const mockCourses: Course[] = [
      {
        id: '1',
        title: 'Full Stack Web Development Bootcamp',
        description: 'Comprehensive course covering React, Node.js, and modern web technologies',
        instructor: 'Alex Rodriguez',
        difficulty: 'Intermediate',
        categories: ['Web Development', 'Full Stack'],
        price: 199.99,
        averageRating: 4.8,
        totalEnrollments: 2500,
        thumbnailUrl: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1172&q=80'
      },
      {
        id: '2',
        title: 'DevOps Mastery: CI/CD and Cloud Deployment',
        description: 'Learn advanced DevOps practices with Docker, Kubernetes, and AWS',
        instructor: 'Sarah Jenkins',
        difficulty: 'Advanced',
        categories: ['DevOps', 'Cloud Computing'],
        price: 249.99,
        averageRating: 4.9,
        totalEnrollments: 1800,
        thumbnailUrl: 'https://images.unsplash.com/photo-1633356122102-3fe601e05bd2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
      },
      {
        id: '3',
        title: 'Python for Data Science and Machine Learning',
        description: 'Practical Python programming with focus on data analysis and AI',
        instructor: 'Dr. Michael Chang',
        difficulty: 'Intermediate',
        categories: ['Programming', 'Data Science'],
        price: 179.99,
        averageRating: 4.7,
        totalEnrollments: 3200,
        thumbnailUrl: 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80'
      }
    ];

    return {
      courses: mockCourses,
      total_count: mockCourses.length,
      total_pages: 1,
      current_page: 1
    };
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
