import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/components/theme-provider';
import { Toaster } from '@/components/ui/toaster';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'CodeMaster LMS - Learn Web Development, Programming & DevOps',
  description: 'Master web development, programming, and DevOps with interactive tutorials, real-world projects, and live mentoring from industry experts.',
  keywords: ['web development', 'programming', 'DevOps', 'coding tutorials', 'online learning'],
  openGraph: {
    title: 'CodeMaster LMS - Learn Web Development, Programming & DevOps',
    description: 'Master web development, programming, and DevOps with interactive tutorials, real-world projects, and live mentoring from industry experts.',
    images: ['/og-image.jpg'],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}