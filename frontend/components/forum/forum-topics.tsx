"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare, ThumbsUp } from "lucide-react";

const topics = [
  {
    id: 1,
    title: "How to implement authentication in Next.js?",
    author: {
      name: "Sarah Johnson",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
    },
    category: "Questions",
    replies: 12,
    likes: 25,
    time: "2 hours ago",
  },
  {
    id: 2,
    title: "Best practices for state management in React",
    author: {
      name: "Michael Chen",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d",
    },
    category: "General",
    replies: 8,
    likes: 15,
    time: "4 hours ago",
  },
  {
    id: 3,
    title: "Feature request: Add dark mode to the platform",
    author: {
      name: "Emily Rodriguez",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80",
    },
    category: "Suggestions",
    replies: 5,
    likes: 32,
    time: "1 day ago",
  },
];

export function ForumTopics() {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">Recent Discussions</h2>
      <div className="space-y-4">
        {topics.map((topic) => (
          <Card key={topic.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-lg font-medium">
                {topic.title}
              </CardTitle>
              <Badge variant="secondary">{topic.category}</Badge>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={topic.author.avatar} />
                    <AvatarFallback>{topic.author.name[0]}</AvatarFallback>
                  </Avatar>
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {topic.author.name}
                    </p>
                    <p className="text-sm text-muted-foreground">
                      {topic.time}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-4 text-muted-foreground">
                  <div className="flex items-center space-x-1">
                    <MessageSquare className="h-4 w-4" />
                    <span className="text-sm">{topic.replies}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <ThumbsUp className="h-4 w-4" />
                    <span className="text-sm">{topic.likes}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}