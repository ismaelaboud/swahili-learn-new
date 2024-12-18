"use client";

import { motion } from "framer-motion";
import { Code2, BookOpen, Users, Cloud, Video, MessageSquare } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const features = [
  {
    icon: Code2,
    title: "Interactive Coding Tutorials",
    description: "Learn by doing with hands-on coding exercises and real-time feedback",
  },
  {
    icon: BookOpen,
    title: "Project-Based Learning",
    description: "Build real-world applications using industry-standard technologies",
  },
  {
    icon: Video,
    title: "Live Mentoring",
    description: "Get guidance from experienced developers in live mentoring sessions",
  },
  {
    icon: Cloud,
    title: "Cloud Infrastructure",
    description: "Practice deployment and DevOps with real cloud environments",
  },
  {
    icon: Users,
    title: "Collaborative Learning",
    description: "Work with peers on group projects and learn from each other",
  },
  {
    icon: MessageSquare,
    title: "Community Support",
    description: "Access our active community forums for help and discussions",
  },
];

export function Features() {
  return (
    <section id="features" className="py-24 bg-muted/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl mb-4">
            Everything you need to become a professional developer
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Our comprehensive platform provides all the tools and resources you need to master modern web development and DevOps.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="h-full">
                <CardHeader>
                  <feature.icon className="h-10 w-10 text-primary mb-4" />
                  <CardTitle>{feature.title}</CardTitle>
                  <CardDescription>{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}