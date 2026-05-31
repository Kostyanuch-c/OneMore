import type { components } from "@/shared/api/schema";

import { apiClient } from "@/shared/api/client";
import { withLocalStorageCache } from "@/shared/lib/local-storage-cache";
import { handleApiResult } from "@/shared/api/response";

export type Subject = components["schemas"]["SubjectOutSchema"];

const SUBJECTS_CACHE_TTL = 60 * 60 * 1000;
const SUBJECTS_STORAGE_KEY = "subjects-cache";

async function getSubjectsFromApi(): Promise<Subject[]> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/subjects/", {});

  return handleApiResult<Subject[]>({
    apiResponse,
    error,
    response,
  });
}

export async function getSubjects(): Promise<Subject[]> {
  return withLocalStorageCache({
    key: SUBJECTS_STORAGE_KEY,
    ttl: SUBJECTS_CACHE_TTL,
    fetcher: getSubjectsFromApi,
  });
}
