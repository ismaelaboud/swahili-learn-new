import { ForumHeader } from "@/components/forum/forum-header";
import { ForumSidebar } from "@/components/forum/forum-sidebar";

export default function ForumLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background">
      <ForumHeader />
      <div className="container mx-auto px-4 py-6">
        <div className="grid lg:grid-cols-[240px_1fr] gap-8">
          <ForumSidebar />
          <main>{children}</main>
        </div>
      </div>
    </div>
  );
}