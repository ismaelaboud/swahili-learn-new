"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import { z } from 'zod';
import { getSession } from '@/lib/auth';
import { getUserProfile, updateUserProfile, User } from '@/lib/api/users';
import { toast } from '@/components/ui/use-toast';

const profileSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  bio: z.string().optional(),
  profilePicture: z.string().url().optional()
});

export default function ProfileEditPage() {
  const [profile, setProfile] = useState<Partial<User>>({});
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const router = useRouter();

  useEffect(() => {
    async function fetchProfile() {
      try {
        const session = await getSession();
        if (!session) {
          router.push('/auth/login');
          return;
        }

        const userProfile = await getUserProfile(session.user.id);
        setProfile(userProfile);
      } catch (error) {
        console.error('Failed to fetch profile', error);
        router.push('/auth/login');
      } finally {
        setLoading(false);
      }
    }

    fetchProfile();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const validatedData = profileSchema.parse(profile);
      
      const session = await getSession();
      if (!session) {
        router.push('/auth/login');
        return;
      }

      await updateUserProfile(session.user.id, validatedData);
      
      toast({
        title: "Profile Updated",
        description: "Your profile has been successfully updated.",
      });
      
      router.push('/dashboard');
    } catch (error) {
      if (error instanceof z.ZodError) {
        const fieldErrors = error.flatten().fieldErrors;
        const errorMap: Record<string, string> = {};
        
        Object.entries(fieldErrors).forEach(([key, messages]) => {
          errorMap[key] = messages[0] || '';
        });
        
        setErrors(errorMap);
      } else {
        console.error('Profile update error', error);
        toast({
          title: "Error",
          description: "An unexpected error occurred while updating your profile.",
          variant: "destructive",
        });
      }
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Edit Profile</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input 
                placeholder="Username" 
                value={profile.username || ''}
                onChange={(e) => setProfile(prev => ({...prev, username: e.target.value}))}
              />
              {errors.username && <p className="text-red-500 text-sm">{errors.username}</p>}
            </div>
            <div>
              <Input 
                placeholder="Bio" 
                value={profile.bio || ''}
                onChange={(e) => setProfile(prev => ({...prev, bio: e.target.value}))}
              />
              {errors.bio && <p className="text-red-500 text-sm">{errors.bio}</p>}
            </div>
            <div>
              <Input 
                placeholder="Profile Picture URL" 
                value={profile.profilePicture || ''}
                onChange={(e) => setProfile(prev => ({...prev, profilePicture: e.target.value}))}
              />
              {errors.profilePicture && <p className="text-red-500 text-sm">{errors.profilePicture}</p>}
            </div>
            <Button type="submit" className="w-full">
              Update Profile
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
