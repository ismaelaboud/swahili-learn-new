"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Menu, X, Code2, User, LogIn, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { getSession, logout } from "@/lib/auth";

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [session, setSession] = useState<any>(null);

  useEffect(() => {
    async function checkSession() {
      const currentSession = await getSession();
      setSession(currentSession);
    }
    checkSession();
  }, []);

  const handleLogout = () => {
    logout();
    setSession(null);
    // Optionally redirect to home or login page
  };

  const menuItems = [
    { href: "#features", label: "Features" },
    { href: "/courses", label: "Courses" },
    { href: "/forum", label: "Forum" },
    { href: "#testimonials", label: "Testimonials" },
    { href: "#pricing", label: "Pricing" },
  ];

  const authItems = session ? [
    { href: "/dashboard", label: "Dashboard", icon: User },
    { href: "#", label: "Logout", onClick: handleLogout, icon: LogOut }
  ] : [
    { href: "/auth/login", label: "Login", icon: LogIn },
    { href: "/auth/register", label: "Register", icon: User }
  ];

  return (
    <nav className="fixed top-0 z-50 w-full bg-background/80 backdrop-blur-md border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <Code2 className="h-8 w-8 text-primary" />
              <span className="font-bold text-xl">CodeMaster</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            {menuItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                {item.label}
              </Link>
            ))}
            
            <div className="flex items-center space-x-4">
              <ThemeToggle />
              {authItems.map((item) => (
                item.onClick ? (
                  <Button 
                    key={item.label} 
                    variant="ghost" 
                    onClick={item.onClick}
                    className="flex items-center space-x-2"
                  >
                    {item.icon && <item.icon className="h-4 w-4" />}
                    <span>{item.label}</span>
                  </Button>
                ) : (
                  <Link 
                    key={item.label} 
                    href={item.href}
                    className="flex items-center space-x-2 hover:text-primary transition-colors"
                  >
                    {item.icon && <item.icon className="h-4 w-4" />}
                    <span>{item.label}</span>
                  </Link>
                )
              ))}
            </div>
          </div>

          <div className="md:hidden flex items-center space-x-4">
            <ThemeToggle />
            <button onClick={() => setIsOpen(!isOpen)}>
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="md:hidden"
        >
          <div className="px-2 pt-2 pb-3 space-y-1 bg-background border-b">
            {[...menuItems, ...authItems].map((item) => (
              item.onClick ? (
                <Button 
                  key={item.label} 
                  variant="ghost" 
                  onClick={item.onClick}
                  className="w-full justify-start flex items-center space-x-2 px-3 py-2"
                >
                  {item.icon && <item.icon className="h-4 w-4 mr-2" />}
                  <span>{item.label}</span>
                </Button>
              ) : (
                <Link
                  key={item.label}
                  href={item.href}
                  className="block px-3 py-2 text-base font-medium text-muted-foreground hover:text-primary flex items-center space-x-2"
                  onClick={() => setIsOpen(false)}
                >
                  {item.icon && <item.icon className="h-4 w-4 mr-2" />}
                  <span>{item.label}</span>
                </Link>
              )
            ))}
          </div>
        </motion.div>
      )}
    </nav>
  );
}