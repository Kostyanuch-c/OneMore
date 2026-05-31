import "server-only";

import type { ApiResponse } from "@/shared/types/api";

import { notFound } from "next/navigation";

import { handleApiResult } from "@/shared/api/response";

export function handleServerApiResult<TData>({
  apiResponse,
  error,
  response,
  notFoundOn404 = false,
}: {
  apiResponse?: ApiResponse<TData>;
  error?: unknown;
  response: Response;
  notFoundOn404?: boolean;
}): TData {
  if (notFoundOn404 && response.status === 404) {
    notFound();
  }

  return handleApiResult<TData>({
    apiResponse,
    error,
    response,
  });
}
