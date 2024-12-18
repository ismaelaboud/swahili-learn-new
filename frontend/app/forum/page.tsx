import { ForumCategories } from "@/components/forum/forum-categories";
import { ForumSearch } from "@/components/forum/forum-search";
import { ForumTopicList } from "@/components/forum/forum-topic-list";

export default function ForumPage() {
  return (
    <div className="space-y-8">
      <ForumSearch />
      <ForumCategories />
      <ForumTopicList />
    </div>
  );
}