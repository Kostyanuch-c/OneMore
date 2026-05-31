import type {
  ProblemListItem,
  SubjectProblemsResult,
} from "@/features/problems/types";

import { apiClient } from "@/shared/api/client";
import { handleApiResult } from "@/shared/api/response";

export type {
  ProblemListItem,
  Problem,
  PaginationOut,
  SubjectProblemsResult,
} from "@/features/problems/types";

export async function getRecentProblems(): Promise<ProblemListItem[]> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/problems/recent/", {});

  const data = handleApiResult<{ items: ProblemListItem[] }>({
    apiResponse,
    error,
    response,
  });

  return data.items;
}

export async function getSubjectProblemsClient(
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

  return handleApiResult<SubjectProblemsResult>({
    apiResponse,
    error,
    response,
  });
}
