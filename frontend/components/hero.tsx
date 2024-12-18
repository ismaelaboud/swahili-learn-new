"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Code2 } from "lucide-react";

export function Hero() {
  return (
    <section className="pt-24 pb-12 lg:pt-32 lg:pb-24 relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h1 className="text-4xl font-bold tracking-tight sm:text-6xl mb-6">
              Master Modern Web Development
              <span className="text-primary"> and DevOps</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              Learn through interactive tutorials, real-world projects, and live mentoring from industry experts. Start your journey to becoming a professional developer today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <Button size="lg" className="group">
                Start Learning
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button size="lg" variant="outline">
                View Courses
              </Button>
            </div>
            <div className="mt-8 flex items-center gap-4 text-muted-foreground">
              <div className="flex -space-x-2">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="relative w-8 h-8 rounded-full overflow-hidden border-2 border-background">
                    <Image
                      src={`https://source.unsplash.com/random/100x100?face&${i}`}
                      alt={`Student ${i}`}
                      fill
                      className="object-cover"
                    />
                  </div>
                ))}
              </div>
              <span>Join 10,000+ students worldwide</span>
            </div>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="relative lg:h-[600px]"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-3xl blur-3xl" />
            <div className="relative bg-card rounded-3xl p-8 shadow-2xl">
              <div className="flex items-center gap-2 mb-4">
                <Code2 className="h-6 w-6 text-primary" />
                <span className="font-semibold">Interactive Learning</span>
              </div>
              <pre className="p-4 bg-muted rounded-lg overflow-x-auto">
                <code className="text-sm">
{`function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// Try it yourself!
console.log(fibonacci(10));`}
                </code>
              </pre>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}