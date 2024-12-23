"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Image from "next/image";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from "@/components/ui/select";

import { 
  fetchCourses, 
  enrollInCourse, 
  Course, 
  CourseSearchParams 
} from "@/lib/api/courses";
import { isAuthenticated } from "@/lib/auth";

export function Courses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<CourseSearchParams>({
    category: "",
    difficulty: "",
    page: 1,
    pageSize: 9
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    async function loadCourses() {
      setLoading(true);
      setError(null);
      try {
        const response = await fetchCourses({
          ...filters,
          query: searchQuery
        });
        
        setCourses(response.courses);
        setTotalPages(response.totalPages);
      } catch (error) {
        console.error("Failed to load courses", error);
        setError(error instanceof Error ? error.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, [searchQuery, filters]);

  // Render loading state
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className="text-center text-red-500 p-8">
        <h3 className="text-2xl font-bold mb-4">Failed to Load Courses</h3>
        <p>{error}</p>
        <Button 
          onClick={() => {
            setError(null);
            setFilters(prev => ({ ...prev }));
          }} 
          className="mt-4"
        >
          Try Again
        </Button>
      </div>
    );
  }

  const handleEnroll = async (courseId: string) => {
    if (!isAuthenticated()) {
      // Redirect to login or show login modal
      return;
    }

    try {
      await enrollInCourse(courseId);
      // Show success notification
    } catch (error) {
      // Show error notification
    }
  };

  const handlePageChange = (newPage: number) => {
    setFilters(prev => ({ ...prev, page: newPage }));
  };

  return (
    <section id="courses" className="py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl mb-4">
            Explore Our Courses
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Find the perfect course to advance your skills and career.
          </p>
        </motion.div>

        {/* Search and Filter Section */}
        <div className="mb-8 flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
          <Input 
            placeholder="Search courses..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-grow"
          />
          <Select 
            value={filters.category || ""}
            onValueChange={(value) => setFilters(prev => ({
              ...prev, 
              category: value === "" ? undefined : value
            }))}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All Categories</SelectItem>
              <SelectItem value="web-development">Web Development</SelectItem>
              <SelectItem value="data-science">Data Science</SelectItem>
              <SelectItem value="cloud-computing">Cloud Computing</SelectItem>
            </SelectContent>
          </Select>
          <Select 
            value={filters.difficulty || ""}
            onValueChange={(value) => setFilters(prev => ({
              ...prev, 
              difficulty: value === "" ? undefined : value
            }))}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Difficulty" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All Levels</SelectItem>
              <SelectItem value="beginner">Beginner</SelectItem>
              <SelectItem value="intermediate">Intermediate</SelectItem>
              <SelectItem value="advanced">Advanced</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {courses.length === 0 ? (
          <div className="text-center py-12">
            No courses found. Try adjusting your search or filters.
          </div>
        ) : (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {courses.map((course, index) => (
                <motion.div
                  key={course.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card className="h-full flex flex-col overflow-hidden">
                    <div className="relative h-48">
                      <Image
                        src={course.thumbnailUrl || "/default-course-image.jpg"}
                        alt={course.title}
                        fill
                        className="object-cover"
                      />
                    </div>
                    <CardHeader className="flex-grow">
                      <CardTitle>{course.title}</CardTitle>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <span>{course.difficulty}</span>
                        <span>•</span>
                        <span>{course.category}</span>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="mb-4 text-sm line-clamp-3">{course.description}</p>
                      <div className="flex justify-between items-center">
                        <div className="flex flex-wrap gap-2">
                          <Badge variant="secondary">
                            {course.price > 0 ? `$${course.price}` : 'Free'}
                          </Badge>
                          <Badge variant="outline">
                            Rating: {course.averageRating.toFixed(1)}/5
                          </Badge>
                        </div>
                        <div className="flex space-x-2">
                          <Link 
                            href={`/courses/${course.id}`} 
                            className="hover:underline text-sm"
                          >
                            View Details
                          </Link>
                          <Button 
                            onClick={() => handleEnroll(course.id)}
                            size="sm"
                            variant="outline"
                          >
                            Enroll
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center mt-8 space-x-2">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                <Button
                  key={page}
                  variant={filters.page === page ? "default" : "outline"}
                  size="sm"
                  onClick={() => handlePageChange(page)}
                >
                  {page}
                </Button>
              ))}
            </div>
          </>
        )}
      </div>
    </section>
  );
}