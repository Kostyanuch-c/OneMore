import type { ProblemListItem } from "@/features/problems/types";

import { Card, CardBody, CardFooter, CardHeader } from "@heroui/card";
import { Chip } from "@heroui/chip";
import { link as linkStyles } from "@heroui/theme";
import clsx from "clsx";
import NextLink from "next/link";

import { getDifficultyColor } from "@/features/problems/lib/difficulty";
import { formatProblemDate } from "@/features/problems/lib/formatProblemDate";

interface RecentProblemCardProps {
  problem: ProblemListItem;
}

function getDetailHref(problem: ProblemListItem): string {
  if (problem.detail_url.startsWith("http")) {
    return problem.detail_url;
  }

  return problem.detail_url || "#";
}

export function RecentProblemCard({ problem }: RecentProblemCardProps) {
  const difficultyColor = getDifficultyColor(problem.difficulty.value);
  const href = getDetailHref(problem);

  return (
    <Card className="h-full">
      <CardHeader className="flex-col items-start gap-2">
        <div className="flex justify-between w-full items-center gap-2">
          <Chip color={difficultyColor} size="sm" variant="flat">
            {problem.difficulty.label}
          </Chip>
          <span className="text-xs text-default-500">
            {formatProblemDate(problem.created_at)}
          </span>
        </div>
        <h4 className="text-base font-semibold leading-5">{problem.title}</h4>
      </CardHeader>
      <CardBody className="pt-0 gap-2">
        <p className="text-sm text-default-600">
          {problem.subject?.name ?? "Без предмета"}
        </p>
        <p className="text-sm text-default-500">
          {problem.section.name} · {problem.topic.name}
        </p>
        {problem.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {problem.tags.map((tag) => (
              <Chip key={tag.id} size="sm" variant="bordered">
                {tag.name}
              </Chip>
            ))}
          </div>
        )}
        <p className="text-sm text-default-500 line-clamp-3">
          {problem.question}
        </p>
      </CardBody>
      <CardFooter>
        <NextLink
          className={clsx(
            linkStyles({ color: "primary" }),
            "w-full text-center text-sm",
          )}
          href={href}
        >
          Открыть задачу
        </NextLink>
      </CardFooter>
    </Card>
  );
}
