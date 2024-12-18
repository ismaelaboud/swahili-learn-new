"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const courses = [
  {
    title: "Full-Stack Web Development",
    level: "Beginner to Advanced",
    duration: "24 weeks",
    image: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97",
    technologies: ["React", "Node.js", "TypeScript", "MongoDB"],
  },
  {
    title: "Cloud DevOps Engineering",
    level: "Intermediate",
    duration: "16 weeks",
    image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
    technologies: ["AWS", "Docker", "Kubernetes", "CI/CD"],
  },
  {
    title: "Frontend Development",
    level: "Beginner",
    duration: "12 weeks",
    image: "https://images.unsplash.com/photo-1593720219276-0b1eacd0aef4",
    technologies: ["HTML", "CSS", "JavaScript", "React"],
  },
];

export function Courses() {
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
            Popular Learning Paths
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Choose from our carefully crafted learning paths designed to take you from beginner to professional.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {courses.map((course, index) => (
            <motion.div
              key={course.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full overflow-hidden">
                <div className="relative h-48">
                  <Image
                    src={course.image}
                    alt={course.title}
                    fill
                    className="object-cover"
                  />
                </div>
                <CardHeader>
                  <CardTitle>{course.title}</CardTitle>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <span>{course.level}</span>
                    <span>•</span>
                    <span>{course.duration}</span>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {course.technologies.map((tech) => (
                      <Badge key={tech} variant="secondary">
                        {tech}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}