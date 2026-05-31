import { getSubjectProblemsServer } from "@/features/problems/api/problem.server";
import { SubjectProblemsClient } from "@/features/problems/ui/SubjectProblemsClient";

const PROBLEMS_PER_PAGE = 8;

interface SubjectProblemsPageProps {
  params: Promise<{
    subjectSlug: string;
  }>;
  searchParams: Promise<{
    page?: string;
  }>;
}

export default async function SubjectProblemsPage({
  params,
  searchParams,
}: SubjectProblemsPageProps) {
  const { subjectSlug } = await params;
  const { page: pageParam } = await searchParams;
  const currentPage = Math.max(1, parseInt(pageParam ?? "1", 10) || 1);

  const initialData = await getSubjectProblemsServer(
    subjectSlug,
    currentPage,
    PROBLEMS_PER_PAGE,
  );

  return (
    <SubjectProblemsClient
      currentPage={currentPage}
      fallbackData={initialData}
      pageSize={PROBLEMS_PER_PAGE}
      subjectSlug={subjectSlug}
    />
  );
}
