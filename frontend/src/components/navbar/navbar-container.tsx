"use client";

import useSWR from "swr";

import { Navbar } from "./navbar";

import { swrKeys } from "@/shared/api/swr-keys";
import { getSubjects } from "@/features/subjects/api/subjects";
import { getCurrentUser } from "@/features/auth/api/auth";

export const NavbarContainer = () => {
  const { data: subjects = [], isLoading: isSubjectsLoading } = useSWR(
    swrKeys.subjects,
    getSubjects,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
    },
  );

  const { data: currentUser = null, isLoading: isCurrentUserLoading } = useSWR(
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

  return (
    <Navbar
      currentUser={currentUser}
      isCurrentUserLoading={isCurrentUserLoading}
      isSubjectsLoading={isSubjectsLoading}
      subjects={subjects}
    />
  );
};
