"use client";

import useSWR from "swr";

import {
  getRecentProblems,
  type ProblemListItem,
} from "@/features/problems/api/problems";
import { ApiRequestError } from "@/shared/api/errors";
import { swrKeys } from "@/shared/api/swr-keys";

export function useRecentProblems() {
  return useSWR<ProblemListItem[], ApiRequestError>(
    swrKeys.recentProblems,
    getRecentProblems,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    },
  );
}
