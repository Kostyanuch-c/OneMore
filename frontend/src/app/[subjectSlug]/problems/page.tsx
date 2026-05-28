import { notFound } from "next/navigation";
import Link from "next/link";

import {
  getSubjectProblems,
  SubjectProblemsNotFoundError,
} from "@/features/problems/api/problems";

type SubjectProblemsPageProps = {
  params: Promise<{
    subjectSlug: string;
  }>;
};

export default async function SubjectProblemsPage({
  params,
}: SubjectProblemsPageProps) {
  const { subjectSlug } = await params;

  try {
    const problems = await getSubjectProblems(subjectSlug);

    return (
      <section className="py-8">
        <h1 className="mb-6 text-2xl font-bold">
          Задачи по предмету: {problems[0]?.subject?.name ?? subjectSlug}
        </h1>

        {problems.length === 0 ? (
          <p className="text-default-600">Пока нет опубликованных задач.</p>
        ) : (
          <ul className="space-y-4">
            {problems.map((problem) => (
              <li
                key={problem.id}
                className="rounded-md border border-default-200 p-4"
              >
                <p className="mb-1 text-sm text-default-500">
                  {problem.difficulty.label}
                </p>

                <h2 className="font-semibold">{problem.title}</h2>

                <p className="mt-2 text-default-600">{problem.question}</p>

                <p className="mt-3">
                  <Link href={`/problems/${problem.id}`}>Открыть задачу</Link>
                </p>
              </li>
            ))}
          </ul>
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
