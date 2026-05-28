import type { components } from "@/shared/api/schema";

import { apiClient } from "@/shared/api/client";

export type Subject = components["schemas"]["SubjectOutSchema"];

export async function getSubjects(): Promise<Subject[]> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/subjects/", {});

  if (!response.ok || error) {
    throw new Error(`Failed to load subjects. Status: ${response.status}`);
  }

  return apiResponse?.data ?? [];
}
