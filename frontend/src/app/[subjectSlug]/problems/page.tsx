import { notFound } from "next/navigation";

import { title, subtitle } from "@/components/primitives";
import { ProblemsPagination } from "@/components/problems/ProblemsPagination";
import { SubjectProblemCard } from "@/components/problems/SubjectProblemCard";
import {
  getSubjectProblems,
  SubjectProblemsNotFoundError,
} from "@/features/problems/api/problems";

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

  try {
    const { items: problems, pagination } = await getSubjectProblems(
      subjectSlug,
      currentPage,
      PROBLEMS_PER_PAGE,
    );

    const totalPages = Math.ceil(pagination.total / PROBLEMS_PER_PAGE);
    const subjectName = problems[0]?.subject?.name ?? subjectSlug;

    return (
      <section className="py-8 max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className={title({ size: "sm", color: "foreground" })}>
            Задачи по предмету
          </h1>
          <p className={subtitle()}>{subjectName}</p>
        </div>

        {problems.length === 0 ? (
          <div className="text-center py-16">
            <p className={subtitle()}>Пока нет опубликованных задач.</p>
          </div>
        ) : (
          <>
            <ul className="space-y-4">
              {problems.map((problem) => (
                <li key={problem.id}>
                  <SubjectProblemCard problem={problem} />
                </li>
              ))}
            </ul>

            <ProblemsPagination
              basePath={`/${subjectSlug}/problems`}
              currentPage={currentPage}
              totalPages={totalPages}
            />
          </>
        )}
      </section>
    );
  } catch (error) {
    if (error instanceof SubjectProblemsNotFoundError) {
      notFound();
    }

    throw error;
  }
}
