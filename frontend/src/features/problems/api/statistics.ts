import type { MainPageStats } from "@/features/problems/types";

import { apiClient } from "@/shared/api/client";
import { handleApiResult } from "@/shared/api/response";

export async function getMainPageStats(): Promise<MainPageStats> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/main_statistics/", {});

  return handleApiResult<MainPageStats>({
    apiResponse,
    error,
    response,
  });
}
