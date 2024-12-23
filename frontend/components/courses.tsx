"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Image from "next/image";
import Link from "next/link";
import { Star } from "lucide-react";
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

interface Course {
  id: string;
  title: string;
  description: string;
  instructor: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  category: string;
  price: number;
  thumbnailUrl: string;
  averageRating: number;
}

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
        
        if (!response || !response.courses) {
          throw new Error('Invalid response from server');
        }

        setCourses(response.courses);
        setTotalPages(response.total_pages || 1);
      } catch (error) {
        console.error("Failed to load courses", error);
        setError(
          error instanceof Error 
            ? error.message 
            : 'An unknown error occurred while fetching courses'
        );
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
        <p className="mb-4">{error}</p>
        <div className="flex justify-center space-x-4">
          <Button 
            onClick={() => {
              setError(null);
              setFilters(prev => ({ ...prev }));
            }} 
            variant="outline"
          >
            Try Again
          </Button>
          <Button 
            onClick={() => {
              setFilters({
                category: "",
                difficulty: "",
                page: 1,
                pageSize: 9
              });
              setSearchQuery("");
            }}
          >
            Reset Filters
          </Button>
        </div>
      </div>
    );
  }

  // Render empty state
  if (courses.length === 0) {
    return (
      <div className="text-center p-8">
        <h3 className="text-2xl font-bold mb-4">No Courses Found</h3>
        <p className="mb-4">There are no courses matching your current filters.</p>
        <Button 
          onClick={() => {
            setFilters({
              category: "",
              difficulty: "",
              page: 1,
              pageSize: 9
            });
            setSearchQuery("");
          }}
        >
          Clear Filters
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

  const filteredCourses = courses.filter(course => 
    course.title.toLowerCase().includes(searchQuery.toLowerCase()) &&
    (filters.category === "" || course.category === filters.category)
  );

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
            value={filters.category || "all"}
            onValueChange={(value) => setFilters(prev => ({
              ...prev,
              category: value === "all" ? "" : value
            }))}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select Category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Categories</SelectItem>
              <SelectItem value="Web Development">Web Development</SelectItem>
              <SelectItem value="DevOps">DevOps</SelectItem>
              <SelectItem value="Programming">Programming</SelectItem>
              <SelectItem value="Data Science">Data Science</SelectItem>
            </SelectContent>
          </Select>
          <Select 
            value={filters.difficulty || "all"}
            onValueChange={(value) => setFilters(prev => ({
              ...prev,
              difficulty: value === "all" ? "" : value
            }))}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select Difficulty" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Levels</SelectItem>
              <SelectItem value="Beginner">Beginner</SelectItem>
              <SelectItem value="Intermediate">Intermediate</SelectItem>
              <SelectItem value="Advanced">Advanced</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {filteredCourses.length === 0 ? (
          <div className="text-center py-12">
            No courses found. Try adjusting your search or filters.
          </div>
        ) : (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredCourses.map((course, index) => (
                <motion.div
                  key={course.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Link href={`/courses/${course.id}`}>
                    <Card className="hover:shadow-lg transition-all duration-300">
                      <div className="relative h-48 w-full">
                        <Image 
                          src={course.thumbnailUrl || "/default-course-image.jpg"} 
                          alt={course.title} 
                          fill 
                          className="object-cover rounded-t-lg"
                        />
                      </div>
                      <CardHeader>
                        <CardTitle>{course.title}</CardTitle>
                        <div className="flex items-center justify-between">
                          <Badge variant="outline">{course.difficulty}</Badge>
                          <span className="text-sm font-semibold">
                            ${course.price.toFixed(2)}
                          </span>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-muted-foreground line-clamp-3">
                          {course.description}
                        </p>
                        <div className="flex justify-between items-center mt-4">
                          <div className="flex items-center space-x-2">
                            <Star className="h-4 w-4 text-yellow-500" />
                            <span className="text-sm">{course.averageRating.toFixed(1)}</span>
                          </div>
                          <Button 
                            size="sm" 
                            variant="outline"
                            onClick={(e) => {
                              e.preventDefault();
                              handleEnroll(course.id);
                            }}
                          >
                            Enroll
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
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