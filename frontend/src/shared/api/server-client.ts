import "server-only";

import type { paths } from "./schema";

import createClient from "openapi-fetch";

const API_BASE_URL =
  process.env.API_INTERNAL_BASE_URL ?? "http://localhost:8000";

export const serverApiClient = createClient<paths>({
  baseUrl: API_BASE_URL,
});
