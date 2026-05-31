"use client";

import useSWR from "swr";

import {
  getSubjectProblemsClient,
  type SubjectProblemsResult,
} from "@/features/problems/api/problems";
import { ApiRequestError } from "@/shared/api/errors";

interface UseSubjectProblemsParams {
  subjectSlug: string;
  currentPage: number;
  pageSize: number;
  fallbackData?: SubjectProblemsResult;
}

export function useSubjectProblems({
  subjectSlug,
  currentPage,
  pageSize,
  fallbackData,
}: UseSubjectProblemsParams) {
  return useSWR<SubjectProblemsResult, ApiRequestError>(
    ["subject", subjectSlug, currentPage, pageSize],
    () => getSubjectProblemsClient(subjectSlug, currentPage, pageSize),
    {
      fallbackData,
      revalidateOnMount: false,
      revalidateIfStale: false,
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    },
  );
}
