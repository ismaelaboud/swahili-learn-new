"use client";

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';
import { z } from 'zod';
import { resetPassword, sendPasswordResetEmail, verifyResetToken } from '@/lib/api/auth';

const emailSchema = z.string().email('Invalid email address');
const passwordSchema = z.string().min(8, 'Password must be at least 8 characters');
const resetTokenSchema = z.string().min(6, 'Reset token must be at least 6 characters');

export default function ResetPasswordPage() {
  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [resetToken, setResetToken] = useState('');
  const [stage, setStage] = useState<'request' | 'verify' | 'reset'>('request');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleRequestReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const validEmail = emailSchema.parse(email);
      await sendPasswordResetEmail(validEmail);
      setSuccess('Password reset email sent. Check your inbox.');
      setStage('verify');
    } catch (err) {
      setError(err instanceof z.ZodError 
        ? 'Invalid email address' 
        : 'Failed to send reset email');
    }
  };

  const handleVerifyToken = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const validEmail = emailSchema.parse(email);
      const validResetToken = resetTokenSchema.parse(resetToken);
      
      await verifyResetToken(validEmail, validResetToken);
      setSuccess('Token verified. You can now reset your password.');
      setStage('reset');
    } catch (err) {
      setError(err instanceof z.ZodError 
        ? 'Invalid reset token' 
        : 'Token verification failed');
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const validEmail = emailSchema.parse(email);
      const validResetToken = resetTokenSchema.parse(resetToken);
      const validPassword = passwordSchema.parse(newPassword);

      await resetPassword(validEmail, validResetToken, validPassword);
      setSuccess('Password reset successfully. You can now log in.');
      
      // Optional: Redirect to login or show login button
    } catch (err) {
      setError(err instanceof z.ZodError 
        ? 'Invalid password' 
        : 'Failed to reset password');
    }
  };

  const renderStage = () => {
    switch (stage) {
      case 'request':
        return (
          <form onSubmit={handleRequestReset} className="space-y-4">
            <Input 
              type="email" 
              placeholder="Enter your email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Button type="submit" className="w-full">
              Send Reset Link
            </Button>
          </form>
        );
      
      case 'verify':
        return (
          <form onSubmit={handleVerifyToken} className="space-y-4">
            <Input 
              type="text" 
              placeholder="Enter reset token" 
              value={resetToken}
              onChange={(e) => setResetToken(e.target.value)}
            />
            <Button type="submit" className="w-full">
              Verify Token
            </Button>
          </form>
        );
      
      case 'reset':
        return (
          <form onSubmit={handleResetPassword} className="space-y-4">
            <Input 
              type="password" 
              placeholder="New Password" 
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <Button type="submit" className="w-full">
              Reset Password
            </Button>
          </form>
        );
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>
          {stage === 'request' 
            ? 'Request Password Reset' 
            : stage === 'verify'
            ? 'Verify Reset Token'
            : 'Reset Your Password'}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {renderStage()}
        
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        {success && <p className="text-green-500 text-sm mt-2">{success}</p>}
      </CardContent>
      <CardFooter>
        <Link 
          href="/auth/login" 
          className="text-sm text-blue-600 hover:underline w-full text-center"
        >
          Back to Login
        </Link>
      </CardFooter>
    </Card>
  );
}
