import { notFound } from "next/navigation";
import { ForumSearch } from "@/components/forum/forum-search";
import { ForumTopicList } from "@/components/forum/forum-topic-list";

const validCategories = ["questions", "suggestions", "general"];

interface CategoryPageProps {
  params: {
    category: string;
  };
}

export default function CategoryPage({ params }: CategoryPageProps) {
  if (!validCategories.includes(params.category)) {
    notFound();
  }

  return (
    <div className="space-y-8">
      <ForumSearch />
      <ForumTopicList category={params.category} />
    </div>
  );
}