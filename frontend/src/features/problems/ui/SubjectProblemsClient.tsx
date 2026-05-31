"use client";

import type { SubjectProblemsResult } from "@/features/problems/api/problems";

import { subtitle, title } from "@/components/primitives";
import { useSubjectProblems } from "@/features/problems/hooks/use-subject-problems";
import { ProblemsPagination } from "@/features/problems/ui/ProblemsPagination";
import { SubjectProblemCard } from "@/features/problems/ui/SubjectProblemCard";

interface SubjectProblemsClientProps {
  subjectSlug: string;
  currentPage: number;
  pageSize: number;
  fallbackData: SubjectProblemsResult;
}

export function SubjectProblemsClient({
  subjectSlug,
  currentPage,
  pageSize,
  fallbackData,
}: SubjectProblemsClientProps) {
  const { data, error, isValidating } = useSubjectProblems({
    subjectSlug,
    currentPage,
    pageSize,
    fallbackData,
  });

  if (error) {
    return (
      <section className="py-8 max-w-4xl mx-auto">
        <p className={subtitle()}>Не удалось загрузить задачи.</p>
      </section>
    );
  }

  const result = data ?? fallbackData;
  const problems = result.items;
  const pagination = result.pagination;

  const totalPages = Math.ceil(pagination.total / pageSize);
  const subjectName = problems[0]?.subject?.name ?? subjectSlug;

  return (
    <section className="py-8 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className={title({ size: "sm", color: "foreground" })}>
          Задачи по предмету
        </h1>
        <p className={subtitle()}>{subjectName}</p>
      </div>

      {isValidating && (
        <p className="mb-4 text-sm text-default-500">Обновляем данные...</p>
      )}

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
}
