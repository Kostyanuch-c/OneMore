"use client";

import { Card, CardBody } from "@heroui/card";
import { Skeleton } from "@heroui/skeleton";

import { useRecentProblems } from "@/features/problems/hooks/use-recent-problems";
import { RecentProblemCard } from "@/features/problems/ui/recent-problem-card";

const RECENT_PROBLEMS_LIMIT = 6;

function RecentProblemsSection() {
  const { data: recentProblems = [], error, isLoading } = useRecentProblems();

  const visibleProblems = recentProblems.slice(0, RECENT_PROBLEMS_LIMIT);

  return (
    <div className="w-full max-w-6xl">
      <div className="flex items-center gap-2 mb-6">
        <span className="text-2xl">📈</span>
        <h2 className="text-2xl font-bold">Последние задачи</h2>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {Array.from({ length: RECENT_PROBLEMS_LIMIT }).map((_, index) => (
            <Card key={index} className="h-full">
              <CardBody className="gap-3">
                <Skeleton className="rounded-lg h-6 w-24" />
                <Skeleton className="rounded-lg h-10 w-full" />
                <Skeleton className="rounded-lg h-4 w-32" />
                <Skeleton className="rounded-lg h-4 w-48" />
                <Skeleton className="rounded-lg h-20 w-full" />
              </CardBody>
            </Card>
          ))}
        </div>
      ) : error ? (
        <Card className="mb-12">
          <CardBody className="text-center text-danger py-10">
            Произошла ошибка при загрузке задач.
          </CardBody>
        </Card>
      ) : visibleProblems.length === 0 ? (
        <Card className="mb-12">
          <CardBody className="text-center text-default-600 py-10">
            Пока нет опубликованных задач.
          </CardBody>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {visibleProblems.map((problem) => (
            <RecentProblemCard key={problem.id} problem={problem} />
          ))}
        </div>
      )}
    </div>
  );
}

export default RecentProblemsSection;
