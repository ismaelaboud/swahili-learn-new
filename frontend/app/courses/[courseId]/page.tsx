import { fetchCourses } from '@/lib/api/courses';
import CourseDetailsClient from './CourseDetailsClient';

export async function generateStaticParams() {
  try {
    const { courses } = await fetchCourses({ pageSize: 100 });
    return courses.map((course) => ({
      courseId: course.id
    }));
  } catch (error) {
    console.error('Failed to generate static params', error);
    return [];
  }
}

export const dynamic = 'force-static';
export const dynamicParams = true;

export default function CourseDetailsPage({ params }: { params: { courseId: string } }) {
  return <CourseDetailsClient params={params} />;
}