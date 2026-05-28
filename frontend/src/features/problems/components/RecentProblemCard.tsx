import type { ProblemListItem } from "@/features/problems/api/problems";

import { Card, CardBody, CardFooter, CardHeader } from "@heroui/card";
import { Chip } from "@heroui/chip";
import { Link } from "@heroui/link";
import { Button } from "@heroui/button";

type RecentProblemCardProps = {
  problem: ProblemListItem;
};

const difficultyColors = {
  easy: "success",
  medium: "warning",
  hard: "danger",
} as const;

function formatDate(dateString: string): string {
  const date = new Date(dateString);

  return date.toLocaleDateString("ru-RU", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

function getDetailHref(problem: ProblemListItem): string {
  if (problem.detail_url.startsWith("http")) {
    return problem.detail_url;
  }

  return problem.detail_url || "#";
}

export function RecentProblemCard({ problem }: RecentProblemCardProps) {
  const difficultyColor =
    difficultyColors[
      problem.difficulty.value as keyof typeof difficultyColors
    ] ?? "default";

  return (
    <Card isPressable as={Link} href={getDetailHref(problem)}>
      <CardHeader className="flex-col items-start gap-2">
        <div className="flex justify-between w-full items-center gap-2">
          <Chip color={difficultyColor} size="sm" variant="flat">
            {problem.difficulty.label}
          </Chip>
          <span className="text-xs text-default-500">
            {formatDate(problem.created_at)}
          </span>
        </div>
        <h4 className="text-base font-semibold leading-5">{problem.title}</h4>
      </CardHeader>
      <CardBody className="pt-0 gap-2">
        <p className="text-sm text-default-600">
          Предмет: {problem.subject?.name ?? "Без предмета"}
        </p>
        <p className="text-sm text-default-600">Тема: {problem.topic.name}</p>
        <p className="text-sm text-default-500 line-clamp-3">
          {problem.question}
        </p>
      </CardBody>
      <CardFooter>
        <Button className="w-full" color="primary" variant="flat">
          Открыть задачу
        </Button>
      </CardFooter>
    </Card>
  );
}
