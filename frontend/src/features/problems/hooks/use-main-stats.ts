"use client";

import type { MainPageStats } from "@/features/problems/types";
import type { ApiRequestError } from "@/shared/api/errors";

import useSWR from "swr";

import { getMainPageStats } from "@/features/problems/api/statistics";
import { swrKeys } from "@/shared/api/swr-keys";

export function useMainStats() {
  return useSWR<MainPageStats, ApiRequestError>(
    swrKeys.mainStats,
    getMainPageStats,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    },
  );
}
