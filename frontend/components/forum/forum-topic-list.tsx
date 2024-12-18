"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare, ThumbsUp } from "lucide-react";

interface Topic {
  id: number;
  title: string;
  author: {
    name: string;
    avatar: string;
  };
  category: string;
  replies: number;
  likes: number;
  time: string;
}

const allTopics: Record<string, Topic[]> = {
  questions: [
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
      id: 4,
      title: "Best way to handle form validation in React?",
      author: {
        name: "David Kim",
        avatar: "https://images.unsplash.com/photo-1599566150163-29194dcaad36",
      },
      category: "Questions",
      replies: 8,
      likes: 15,
      time: "5 hours ago",
    },
  ],
  suggestions: [
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
    {
      id: 5,
      title: "Suggestion: Add code playground feature",
      author: {
        name: "Alex Turner",
        avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e",
      },
      category: "Suggestions",
      replies: 15,
      likes: 45,
      time: "3 days ago",
    },
  ],
  general: [
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
      id: 6,
      title: "Share your developer setup and tools",
      author: {
        name: "Lisa Wang",
        avatar: "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f",
      },
      category: "General",
      replies: 20,
      likes: 28,
      time: "2 days ago",
    },
  ],
};

interface ForumTopicListProps {
  category?: string;
}

export function ForumTopicList({ category }: ForumTopicListProps) {
  const topics = category ? allTopics[category] : Object.values(allTopics).flat();

  const categoryTitle = category
    ? category.charAt(0).toUpperCase() + category.slice(1)
    : "Recent Discussions";

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight">{categoryTitle}</h2>
        <span className="text-sm text-muted-foreground">
          {topics.length} {topics.length === 1 ? "topic" : "topics"}
        </span>
      </div>
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