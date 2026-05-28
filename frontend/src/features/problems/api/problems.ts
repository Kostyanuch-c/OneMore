import type {
  ProblemListItem,
  SubjectProblemsResult,
} from "@/features/problems/types";

import { apiClient } from "@/shared/api/client";

export type {
  ProblemListItem,
  Problem,
  PaginationOut,
  SubjectProblemsResult,
} from "@/features/problems/types";

export class SubjectProblemsNotFoundError extends Error {
  readonly status = 404;

  constructor(subjectSlug: string) {
    super(`Subject not found: ${subjectSlug}`);
    this.name = "SubjectProblemsNotFoundError";
  }
}

export async function getRecentProblems(): Promise<ProblemListItem[]> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/problems/recent/", {});

  if (!response.ok || error) {
    throw new Error(
      `Failed to load recent problems. Status: ${response.status}`,
    );
  }

  return apiResponse?.data?.items ?? [];
}

export async function getSubjectProblems(
  subjectSlug: string,
  page = 1,
  limit = 10,
): Promise<SubjectProblemsResult> {
  const offset = (page - 1) * limit;

  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/subjects/{subject_slug}/problems/", {
    params: {
      path: {
        subject_slug: subjectSlug,
      },
      query: {
        offset,
        limit,
      },
    },
  });

  if (response.status === 404) {
    throw new SubjectProblemsNotFoundError(subjectSlug);
  }

  if (!response.ok || error) {
    throw new Error(
      `Failed to load subject problems for "${subjectSlug}". Status: ${response.status}`,
    );
  }

  const data = apiResponse?.data;

  return {
    items: data?.items ?? [],
    pagination: data?.pagination ?? { offset, limit, total: 0 },
  };
}
