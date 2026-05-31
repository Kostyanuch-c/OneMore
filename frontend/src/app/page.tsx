"use client";

import useSWR from "swr";
import { Card, CardBody } from "@heroui/card";
import { Skeleton } from "@heroui/skeleton";

import { title, subtitle } from "@/components/primitives";
import { RecentProblemCard } from "@/features/problems/ui/RecentProblemCard";
import { TutoringCTA } from "@/components/tutoring-cta";
import { getRecentProblems } from "@/features/problems/api/problems";
import { swrKeys } from "@/shared/api/swr-keys";

export default function Home() {
  const {
    data: recentProblems = [],
    isLoading,
    error,
  } = useSWR(swrKeys.recentProblems, getRecentProblems, {
    revalidateOnFocus: false,
    revalidateOnReconnect: true,
  });

  const visibleProblems = recentProblems.slice(0, 6);

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      {/* Hero Section */}
      <div className="inline-block max-w-4xl text-center justify-center mb-8">
        <h1 className="text-4xl lg:text-5xl font-bold mb-4">
          Добро пожаловать на платформу{" "}
          <span className={title({ color: "blue" })}>ХимРепетитор</span>
        </h1>
        <p className={subtitle()}>
          Подробные разборы задач по химии с пошаговыми решениями и понятными
          объяснениями
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl mb-12">
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl font-bold text-primary mb-2">5</div>
            <div className="text-default-600">Задач с решениями</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl font-bold text-primary mb-2">5</div>
            <div className="text-default-600">Тематических разделов</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody className="text-center">
            <div className="text-4xl font-bold text-primary mb-2">100%</div>
            <div className="text-default-600">Проверенных решений</div>
          </CardBody>
        </Card>
      </div>

      {/* Recent Problems */}
      <div className="w-full max-w-6xl">
        <div className="flex items-center gap-2 mb-6">
          <span className="text-2xl">📈</span>
          <h2 className="text-2xl font-bold">Последние задачи</h2>
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="h-full">
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
          <Card>
            <CardBody className="text-center text-danger py-10">
              Произошла ошибка при загрузке задач.
            </CardBody>
          </Card>
        ) : visibleProblems.length === 0 ? (
          <Card>
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

      <div className="w-full max-w-6xl">
        <TutoringCTA />
      </div>
    </section>
  );
}
