import type { paths } from "./schema";

import createClient from "openapi-fetch";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export const apiClient = createClient<paths>({
  baseUrl: API_BASE_URL,
  fetch: (input: RequestInfo | URL, init?: RequestInit) =>
    fetch(input, {
      ...init,
      credentials: "include",
    }),
});

export type ApiClient = typeof apiClient;
