"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getUserProfile } from '@/lib/api/users';
import { getSession } from '@/lib/auth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function DashboardPage() {
  const [userProfile, setUserProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function fetchUserProfile() {
      try {
        const session = await getSession();
        if (!session) {
          router.push('/auth/login');
          return;
        }

        const profile = await getUserProfile(session.user.id);
        setUserProfile(profile);
      } catch (error) {
        console.error('Failed to fetch profile', error);
        router.push('/auth/login');
      } finally {
        setLoading(false);
      }
    }

    fetchUserProfile();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!userProfile) {
    return <div>Unable to load profile</div>;
  }

  return (
    <div className="container mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>My Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h2 className="text-xl font-bold">Welcome, {userProfile.username}!</h2>
              <p>Role: {userProfile.role}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle>My Courses</CardTitle>
                </CardHeader>
                <CardContent>
                  <Link href="/courses">
                    <Button variant="outline" className="w-full">
                      Browse Courses
                    </Button>
                  </Link>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Profile</CardTitle>
                </CardHeader>
                <CardContent>
                  <Link href="/dashboard/profile">
                    <Button variant="outline" className="w-full">
                      Edit Profile
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            </div>

            {userProfile.role === 'INSTRUCTOR' && (
              <Card>
                <CardHeader>
                  <CardTitle>Instructor Tools</CardTitle>
                </CardHeader>
                <CardContent>
                  <Link href="/instructor/courses">
                    <Button variant="outline" className="w-full">
                      Manage Courses
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
