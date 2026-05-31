import type { components } from "@/shared/api/schema";

export type ApiErrorItem = components["schemas"]["ApiError"];

export interface ApiResponse<TData = unknown> {
  data?: TData | null;
  meta?: Record<string, unknown>;
  errors?: ApiErrorItem[];
}
