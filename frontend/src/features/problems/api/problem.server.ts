import "server-only";

import type { SubjectProblemsResult } from "@/features/problems/types";

import { serverApiClient } from "@/shared/api/server-client";
import { handleServerApiResult } from "@/shared/api/server-response";

export async function getSubjectProblemsServer(
  subjectSlug: string,
  page = 1,
  limit = 10,
): Promise<SubjectProblemsResult> {
  const offset = (page - 1) * limit;

  const {
    data: apiResponse,
    error,
    response,
  } = await serverApiClient.GET("/api/v1/subjects/{subject_slug}/problems/", {
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

  return handleServerApiResult<SubjectProblemsResult>({
    apiResponse,
    error,
    response,
    notFoundOn404: true,
  });
}
