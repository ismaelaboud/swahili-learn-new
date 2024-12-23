"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import { z } from 'zod';
import { registerUser } from '@/lib/api/users';
import { toast } from '@/components/ui/use-toast';

const registrationSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  role: z.enum(['STUDENT', 'INSTRUCTOR'])
});

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'STUDENT'
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setIsSubmitting(true);
    
    try {
      const validatedData = registrationSchema.parse(formData);
      
      const result = await registerUser(validatedData);
      
      toast({
        title: 'Registration Successful',
        description: 'You have been registered successfully.',
        variant: 'default'
      });
      
      // Redirect to login or dashboard
      router.push('/auth/login');
    } catch (error) {
      setIsSubmitting(false);
      
      if (error instanceof z.ZodError) {
        const fieldErrors = error.flatten().fieldErrors;
        const errorMap: Record<string, string> = {};
        
        Object.entries(fieldErrors).forEach(([key, messages]) => {
          errorMap[key] = messages[0] || '';
        });
        
        setErrors(errorMap);
      } else {
        // Handle API or network errors
        const errorMessage = error instanceof Error 
          ? error.message 
          : 'An unexpected error occurred';
        
        toast({
          title: 'Registration Error',
          description: errorMessage,
          variant: 'destructive'
        });
      }
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Register for Swahili Learn</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input 
                placeholder="Username" 
                value={formData.username}
                onChange={(e) => setFormData(prev => ({...prev, username: e.target.value}))}
              />
              {errors.username && <p className="text-red-500 text-sm mt-1">{errors.username}</p>}
            </div>
            <div>
              <Input 
                type="email" 
                placeholder="Email" 
                value={formData.email}
                onChange={(e) => setFormData(prev => ({...prev, email: e.target.value}))}
              />
              {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
            </div>
            <div>
              <Input 
                type="password" 
                placeholder="Password" 
                value={formData.password}
                onChange={(e) => setFormData(prev => ({...prev, password: e.target.value}))}
              />
              {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password}</p>}
            </div>
            <div>
              <Select 
                value={formData.role}
                onValueChange={(value) => setFormData(prev => ({...prev, role: value as 'STUDENT' | 'INSTRUCTOR'}))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select Role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="STUDENT">Student</SelectItem>
                  <SelectItem value="INSTRUCTOR">Instructor</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button 
              type="submit" 
              className="w-full" 
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Registering...' : 'Register'}
            </Button>
          </form>
        </CardContent>
        <CardFooter>
          <Link 
            href="/auth/login" 
            className="text-sm text-blue-600 hover:underline w-full text-center"
          >
            Already have an account? Login
          </Link>
        </CardFooter>
      </Card>
    </div>
  );
}
