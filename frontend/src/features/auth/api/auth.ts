import type { components } from "@/shared/api/schema";

import { mutate } from "swr";

import { apiClient } from "@/shared/api/client";
import { getCsrfHeaders } from "@/shared/api/csrf";
import { swrKeys } from "@/shared/api/swr-keys";
import { handleApiResult, handleEmptyApiResult } from "@/shared/api/response";

export type CurrentUser = components["schemas"]["UserOutSchema"];
export type RequestLoginCodeInput = components["schemas"]["AuthInputSchema"];
export type RequestLoginCodeResponse = components["schemas"]["AuthOutSchema"];
export type ConfirmLoginCodeInput =
  components["schemas"]["ConfirmEmailInputSchema"];
export type ConfirmLoginCodeResponse =
  components["schemas"]["AuthUserOutSchema"];

export async function getCurrentUser(): Promise<CurrentUser | null> {
  const {
    data: apiResponse,
    error,
    response,
  } = await apiClient.GET("/api/v1/profile/me/", {});

  if (response.status === 401 || response.status === 403) {
    return null;
  }

  return handleApiResult<CurrentUser>({
    apiResponse,
    error,
    response,
  });
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

  return handleApiResult<RequestLoginCodeResponse>({
    apiResponse,
    error,
    response,
  });
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

  const data = handleApiResult<ConfirmLoginCodeResponse>({
    apiResponse,
    error,
    response,
  });

  await mutate(swrKeys.currentUser, data.user, { revalidate: false });

  return data;
}

export async function logout(): Promise<void> {
  const { error, response } = await apiClient.POST("/api/v1/auth/logout/", {
    headers: getCsrfHeaders(),
  });

  handleEmptyApiResult({
    error,
    response,
  });

  await mutate(swrKeys.currentUser, null, { revalidate: false });
}
