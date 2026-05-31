"use client";

import useSWR from "swr";

import { getCurrentUser, type CurrentUser } from "@/features/auth/api/auth";
import { ApiRequestError } from "@/shared/api/errors";
import { swrKeys } from "@/shared/api/swr-keys";

export function useCurrentUser() {
  return useSWR<CurrentUser | null, ApiRequestError>(
    swrKeys.currentUser,
    getCurrentUser,
    {
      refreshInterval: 0,
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      shouldRetryOnError: false,
      dedupingInterval: 5000,
    },
  );
}
