"use client";

import Link from "next/link";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { MessageSquare, Lightbulb, Users } from "lucide-react";

const categories = [
  {
    title: "Questions",
    icon: MessageSquare,
    href: "/forum/questions",
  },
  {
    title: "Suggestions",
    icon: Lightbulb,
    href: "/forum/suggestions",
  },
  {
    title: "General",
    icon: Users,
    href: "/forum/general",
  },
];

export function ForumSidebar() {
  return (
    <nav className="sticky top-20 h-[calc(100vh-5rem)] overflow-y-auto py-6 pr-6 lg:py-8">
      <div className="space-y-4">
        <div className="px-3 py-2">
          <h2 className="mb-2 px-4 text-lg font-semibold">Categories</h2>
          <div className="space-y-1">
            {categories.map((category) => (
              <Button
                key={category.title}
                variant="ghost"
                className="w-full justify-start"
                asChild
              >
                <Link href={category.href}>
                  <category.icon className="mr-2 h-4 w-4" />
                  {category.title}
                </Link>
              </Button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}