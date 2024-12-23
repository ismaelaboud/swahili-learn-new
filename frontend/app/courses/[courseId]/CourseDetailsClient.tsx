"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
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
import { Clock, BookOpen, Star, Users } from 'lucide-react';
import { useToast } from '@/components/ui/use-toast';

interface CourseDetailsClientProps {
  params: { courseId: string };
}

export default function CourseDetailsClient({ params }: CourseDetailsClientProps) {
  const router = useRouter();
  const { toast, ToastComponent } = useToast();

  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCourseDetails() {
      if (!params.courseId) return;

      try {
        setLoading(true);
        const courseData = await getCourseDetails(params.courseId);
        setCourse(courseData);
      } catch (fetchError) {
        console.error('Failed to load course details', fetchError);
        setError('Failed to load course details. Please try again later.');
        toast({
          title: 'Error',
          description: 'Failed to load course details',
          variant: 'destructive'
        });
      } finally {
        setLoading(false);
      }
    }

    loadCourseDetails();
  }, [params.courseId, toast]);

  const handleEnroll = async () => {
    if (!isAuthenticated()) {
      router.push('/auth/login');
      return;
    }

    if (!course) return;

    try {
      await enrollInCourse(course.id);
      toast({
        title: 'Success',
        description: 'Successfully enrolled in the course',
        variant: 'default'
      });
    } catch (error) {
      toast({
        title: 'Enrollment Error',
        description: 'Failed to enroll in the course',
        variant: 'destructive'
      });
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
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
    <>
      {ToastComponent}
      <div className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Course Image and Metadata */}
          <div className="md:col-span-2">
            <div className="relative h-96 mb-6">
              <Image 
                src={course.thumbnailUrl || "/default-course-image.jpg"} 
                alt={course.title} 
                fill 
                className="object-cover rounded-lg"
              />
            </div>
            
            <h1 className="text-3xl font-bold mb-4">{course.title}</h1>
            <p className="text-muted-foreground mb-6">{course.description}</p>

            {/* Course Metadata */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="flex items-center space-x-2">
                <Users className="h-5 w-5 text-primary" />
                <span>{course.totalEnrollments} Enrolled</span>
              </div>
              <div className="flex items-center space-x-2">
                <Star className="h-5 w-5 text-yellow-500" />
                <span>{course.averageRating.toFixed(1)} Rating</span>
              </div>
              <div className="flex items-center space-x-2">
                <BookOpen className="h-5 w-5 text-green-500" />
                <span>{course.difficulty} Level</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="h-5 w-5 text-blue-500" />
                <span>${course.price.toFixed(2)}</span>
              </div>
            </div>

            <Button 
              onClick={handleEnroll} 
              className="w-full"
              disabled={loading}
            >
              Enroll Now
            </Button>
          </div>

          {/* Sidebar */}
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Course Details</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Instructor</span>
                    <span className="font-semibold">{course.instructor}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Categories</span>
                    <div className="flex space-x-2">
                      {course.categories.map(category => (
                        <Badge key={category} variant="outline">{category}</Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </>
  );
}
