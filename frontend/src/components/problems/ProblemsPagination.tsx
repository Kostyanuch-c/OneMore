"use client";

import { Pagination } from "@heroui/pagination";
import { useRouter } from "next/navigation";

type ProblemsPaginationProps = {
  currentPage: number;
  totalPages: number;
  basePath: string;
};

export function ProblemsPagination({
  currentPage,
  totalPages,
  basePath,
}: ProblemsPaginationProps) {
  const router = useRouter();

  if (totalPages <= 1) return null;

  return (
    <div className="flex justify-center mt-8">
      <Pagination
        showControls
        page={currentPage}
        total={totalPages}
        onChange={(page) => router.push(`${basePath}?page=${page}`)}
      />
    </div>
  );
}
