"use client";

import useSWR from "swr";

import { getSubjects, type Subject } from "@/features/subjects/api/subjects";
import { ApiRequestError } from "@/shared/api/errors";
import { swrKeys } from "@/shared/api/swr-keys";

export function useSubjects() {
  return useSWR<Subject[], ApiRequestError>(swrKeys.subjects, getSubjects, {
    revalidateOnFocus: false,
    revalidateOnReconnect: true,
  });
}
