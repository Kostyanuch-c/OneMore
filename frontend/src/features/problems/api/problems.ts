import type { components } from "@/shared/api/schema";

import { apiClient } from "@/shared/api/client";

export type ProblemListItem = components["schemas"]["ProblemListItemOutSchema"];

export type Problem = components["schemas"]["ProblemOutSchema"];

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
): Promise<Problem[]> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/subjects/{subject_slug}/problems/", {
    params: {
      path: {
        subject_slug: subjectSlug,
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

  return apiResponse?.data?.items ?? [];
}
