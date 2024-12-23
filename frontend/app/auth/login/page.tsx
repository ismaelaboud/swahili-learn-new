"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { login } from '@/lib/auth';
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters')
});

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{email?: string, password?: string, general?: string}>({});
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const validatedData = loginSchema.parse({ email, password });
      
      const session = await login(validatedData.email, validatedData.password);
      
      if (session) {
        // Redirect based on user role
        switch (session.user.role) {
          case 'ADMIN':
            router.push('/admin/dashboard');
            break;
          case 'INSTRUCTOR':
            router.push('/instructor/dashboard');
            break;
          default:
            router.push('/dashboard');
        }
      } else {
        // Show login error
        setErrors({ general: 'Invalid credentials' });
      }
    } catch (error) {
      if (error instanceof z.ZodError) {
        const fieldErrors = error.flatten().fieldErrors;
        setErrors({
          email: fieldErrors.email?.[0],
          password: fieldErrors.password?.[0]
        });
      } else {
        console.error('Login error', error);
        setErrors({ general: 'An unexpected error occurred' });
      }
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Login to Swahili Learn</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Input 
              type="email" 
              placeholder="Email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}
          </div>
          <div>
            <Input 
              type="password" 
              placeholder="Password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {errors.password && <p className="text-red-500 text-sm">{errors.password}</p>}
          </div>
          {errors.general && <p className="text-red-500 text-sm">{errors.general}</p>}
          <Button type="submit" className="w-full">Login</Button>
        </form>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Link href="/auth/reset-password" className="text-sm text-blue-600 hover:underline">
          Forgot Password?
        </Link>
        <Link href="/auth/register" className="text-sm text-blue-600 hover:underline">
          Create Account
        </Link>
      </CardFooter>
    </Card>
  );
}
