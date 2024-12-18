"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { MessageSquarePlus, Bell } from "lucide-react";

export function ForumHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link href="/forum" className="mr-6 flex items-center space-x-2">
            <span className="font-bold">CodeMaster Forum</span>
          </Link>
        </div>
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="flex items-center space-x-2">
            <Button variant="ghost" size="icon">
              <Bell className="h-4 w-4" />
            </Button>
            <ThemeToggle />
            <Button>
              <MessageSquarePlus className="mr-2 h-4 w-4" />
              New Post
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}