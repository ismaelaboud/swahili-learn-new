import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export default function CreateCoursePage() {
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Implement course creation logic
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Create New Course</h1>
      <form onSubmit={handleSubmit} className="max-w-2xl space-y-6">
        <div>
          <Label>Course Title</Label>
          <Input 
            placeholder="Enter course title" 
            required 
          />
        </div>

        <div>
          <Label>Description</Label>
          <Textarea 
            placeholder="Provide a detailed course description" 
            required 
            rows={4} 
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <Label>Category</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="web-dev">Web Development</SelectItem>
                <SelectItem value="devops">DevOps</SelectItem>
                <SelectItem value="programming">Programming</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label>Difficulty Level</Label>
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="Select difficulty" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="beginner">Beginner</SelectItem>
                <SelectItem value="intermediate">Intermediate</SelectItem>
                <SelectItem value="advanced">Advanced</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div>
          <Label>Price</Label>
          <Input 
            type="number" 
            placeholder="Course price" 
            min="0" 
            step="0.01" 
          />
        </div>

        <Button type="submit" className="w-full">Create Course</Button>
      </form>
    </div>
  );
}
