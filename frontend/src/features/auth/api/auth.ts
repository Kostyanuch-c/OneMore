import type { components } from "@/shared/api/schema";

import { mutate } from "swr";

import { apiClient } from "@/shared/api/client";
import { getCsrfHeaders } from "@/shared/api/csrf";
import { swrKeys } from "@/shared/api/swr-keys";

export type CurrentUser = components["schemas"]["UserOutSchema"];
export type RequestLoginCodeInput = components["schemas"]["AuthInputSchema"];
export type RequestLoginCodeResponse = components["schemas"]["AuthOutSchema"];
export type ConfirmLoginCodeInput =
  components["schemas"]["ConfirmEmailInputSchema"];
export type ConfirmLoginCodeResponse =
  components["schemas"]["AuthUserOutSchema"];

export async function getCurrentUser(): Promise<CurrentUser | null> {
  const { data: apiResponse, response } = await apiClient.GET(
    "/api/v1/profile/me/",
    {},
  );

  if (response.status === 401 || response.status === 403) {
    return null;
  }

  if (!response.ok) {
    throw new Error(`Failed to load current user. Status: ${response.status}`);
  }

  return apiResponse?.data ?? null;
}

export async function requestLoginCode(
  input: RequestLoginCodeInput,
): Promise<RequestLoginCodeResponse> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.POST("/api/v1/auth/login/code/", {
    body: input,
    headers: getCsrfHeaders(),
  });

  if (!response.ok || error) {
    throw new Error(`Failed to request login code. Status: ${response.status}`);
  }

  if (!apiResponse?.data) {
    throw new Error("Request login code response is empty.");
  }

  return apiResponse.data;
}

export async function confirmLoginCode(
  input: ConfirmLoginCodeInput,
): Promise<ConfirmLoginCodeResponse> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.POST("/api/v1/auth/login/confirm/", {
    body: input,
    headers: getCsrfHeaders(),
  });

  if (!response.ok || error) {
    throw new Error(`Failed to confirm login code. Status: ${response.status}`);
  }

  if (!apiResponse?.data) {
    throw new Error("Confirm login code response is empty.");
  }

  const data = apiResponse.data;

  await mutate(swrKeys.currentUser, data.user, { revalidate: false });

  return data;
}

export async function logout(): Promise<void> {
  const { error, response } = await apiClient.POST("/api/v1/auth/logout/", {
    headers: getCsrfHeaders(),
  });

  if (!response.ok || error) {
    throw new Error(`Failed to logout. Status: ${response.status}`);
  }

  await mutate(swrKeys.currentUser, null, { revalidate: false });
}
