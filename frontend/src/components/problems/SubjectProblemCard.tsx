import type { Problem } from "@/features/problems/types";

import { Card, CardBody, CardFooter, CardHeader } from "@heroui/card";
import { Chip } from "@heroui/chip";
import { link as linkStyles } from "@heroui/theme";
import clsx from "clsx";
import NextLink from "next/link";

import { getDifficultyColor } from "@/features/problems/lib/difficulty";
import { formatProblemDate } from "@/features/problems/lib/formatProblemDate";

type SubjectProblemCardProps = {
  problem: Problem;
};

export function SubjectProblemCard({ problem }: SubjectProblemCardProps) {
  const difficultyColor = getDifficultyColor(problem.difficulty.value);
  const author = problem.author?.full_name ?? problem.author?.username;

  return (
    <Card className="w-full">
      <CardHeader className="flex-col items-start gap-2 pb-2">
        <div className="flex flex-wrap justify-between w-full items-center gap-2">
          <Chip color={difficultyColor} size="sm" variant="flat">
            {problem.difficulty.label}
          </Chip>
          <span className="text-xs text-default-500">
            {formatProblemDate(problem.created_at)}
          </span>
        </div>
        <h3 className="text-lg font-semibold leading-6">{problem.title}</h3>
        <div className="flex flex-wrap gap-x-4 gap-y-1 text-sm text-default-500">
          {problem.subject && <span>{problem.subject.name}</span>}
          <span>{problem.section.name}</span>
          <span>{problem.topic.name}</span>
          {author && <span>Автор: {author}</span>}
        </div>
      </CardHeader>
      <CardBody className="pt-0 gap-2">
        {problem.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-1">
            {problem.tags.map((tag) => (
              <Chip key={tag.id} size="sm" variant="bordered">
                {tag.name}
              </Chip>
            ))}
          </div>
        )}
        <p className="text-sm text-default-600 line-clamp-4">
          {problem.question}
        </p>
      </CardBody>
      <CardFooter className="pt-0">
        <NextLink
          className={clsx(linkStyles({ color: "primary" }), "text-sm font-medium")}
          href={`/problems/${problem.id}`}
        >
          Открыть задачу →
        </NextLink>
      </CardFooter>
    </Card>
  );
}
