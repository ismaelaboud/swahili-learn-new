"use client";

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  getCourseDetails, 
  enrollInCourse, 
  Course 
} from '@/lib/api/courses';
import { isAuthenticated } from '@/lib/auth';

export default function CourseDetailsPage() {
  const params = useParams();
  const courseId = Array.isArray(params.courseId) 
    ? params.courseId[0] 
    : params.courseId;

  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCourseDetails() {
      if (!courseId) return;

      try {
        setLoading(true);
        const courseData = await getCourseDetails(courseId);
        setCourse(courseData);
      } catch (fetchError) {
        console.error('Failed to load course details', fetchError);
        setError('Failed to load course details. Please try again later.');
      } finally {
        setLoading(false);
      }
    }

    loadCourseDetails();
  }, [courseId]);

  const handleEnroll = async () => {
    if (!isAuthenticated()) {
      // Redirect to login or show login modal
      return;
    }

    if (!course) return;

    try {
      await enrollInCourse(course.id);
      // Show success notification
    } catch (error) {
      // Show error notification
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        Loading course details...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen text-red-500">
        {error}
      </div>
    );
  }

  if (!course) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        Course not found
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="grid md:grid-cols-2 gap-8">
        {/* Course Image */}
        <div className="relative h-96">
          <Image 
            src={course.thumbnailUrl || "/default-course-image.jpg"} 
            alt={course.title} 
            fill 
            className="object-cover rounded-lg"
          />
        </div>

        {/* Course Details */}
        <Card>
          <CardHeader>
            <CardTitle>{course.title}</CardTitle>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Badge variant="outline">{course.difficulty}</Badge>
              <Badge variant="outline">{course.category}</Badge>
            </div>
          </CardHeader>
          <CardContent>
            <p className="mb-4">{course.description}</p>

            <div className="space-y-4">
              <div className="flex justify-between">
                <span>Instructor:</span>
                <span>{course.instructor}</span>
              </div>
              <div className="flex justify-between">
                <span>Price:</span>
                <span>{course.price > 0 ? `$${course.price}` : 'Free'}</span>
              </div>
              <div className="flex justify-between">
                <span>Average Rating:</span>
                <span>{course.averageRating.toFixed(1)}/5</span>
              </div>
              <div className="flex justify-between">
                <span>Total Enrollments:</span>
                <span>{course.totalEnrollments}</span>
              </div>
            </div>

            <div className="mt-6 flex space-x-4">
              <Button 
                onClick={handleEnroll} 
                className="w-full"
              >
                Enroll Now
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
