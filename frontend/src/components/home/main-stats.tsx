"use client";

import { Card, CardBody } from "@heroui/card";
import { Skeleton } from "@heroui/skeleton";

import { useMainStats } from "@/features/problems/hooks/use-main-stats";
import { formatNumber } from "@/shared/lib/format-number";

function MainStats() {
  const {
    data: mainStats,
    error: mainStatsError,
    isLoading: isLoadingMainStats,
  } = useMainStats();

  if (mainStatsError) {
    return null;
  }

  if (isLoadingMainStats || !mainStats) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full max-w-6xl mb-12">
        {Array.from({ length: 4 }).map((_, index) => (
          <Card key={index}>
            <CardBody className="text-center">
              <Skeleton className="mx-auto mb-2 h-10 w-20 rounded-lg" />
              <Skeleton className="mx-auto h-5 w-36 rounded-lg" />
            </CardBody>
          </Card>
        ))}
      </div>
    );
  }

  const statsItems = [
    {
      value: mainStats.total_problems,
      label: "Задачи для практики",
      description: "по всем предметам платформы",
    },
    {
      value: mainStats.total_solutions,
      label: "Разобранные решения",
      description: "с пошаговыми объяснениями",
    },
    {
      value: mainStats.total_sections,
      label: "Разделы программы",
      description: "для структурного обучения",
    },
    {
      value: mainStats.total_topics,
      label: "Темы внутри разделов",
      description: "для точечной подготовки",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 w-full max-w-6xl mb-12">
      {statsItems.map((item) => (
        <Card key={item.label}>
          <CardBody className="text-center gap-1">
            <div className="text-4xl font-bold text-primary">
              {formatNumber(item.value)}
            </div>
            <div className="text-base font-medium text-default-700">
              {item.label}
            </div>
            <div className="text-small text-default-500">
              {item.description}
            </div>
          </CardBody>
        </Card>
      ))}
    </div>
  );
}

export default MainStats;
