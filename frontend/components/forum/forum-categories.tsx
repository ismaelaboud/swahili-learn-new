"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare, Lightbulb, Users } from "lucide-react";

const categories = [
  {
    title: "Questions",
    description: "Get help with coding problems and technical challenges",
    icon: MessageSquare,
    count: 2345,
    color: "text-blue-500",
  },
  {
    title: "Suggestions",
    description: "Share ideas and suggest improvements",
    icon: Lightbulb,
    count: 892,
    color: "text-yellow-500",
  },
  {
    title: "General Discussion",
    description: "Connect with other developers and share experiences",
    icon: Users,
    count: 1563,
    color: "text-green-500",
  },
];

export function ForumCategories() {
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {categories.map((category) => (
        <Card key={category.title} className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center space-x-4">
            <category.icon className={`h-8 w-8 ${category.color}`} />
            <div>
              <CardTitle className="text-xl">{category.title}</CardTitle>
              <p className="text-sm text-muted-foreground mt-1">
                {category.count.toLocaleString()} discussions
              </p>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{category.description}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}