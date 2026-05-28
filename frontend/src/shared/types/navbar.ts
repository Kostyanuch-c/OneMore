import type { Subject } from "@/features/subjects/api/subjects";

export type NavItemConfig = {
  label: string;
  href: string;
};

export type ProblemsDropdownProps = {
  subjects: Subject[];
  isProblemsPage: boolean;
  onSelectProblemSubject: (subjectSlug: string) => void;
};

export type MobileProblemsMenuListProps = {
  subjects: Subject[];
  onCloseMenu: () => void;
};
