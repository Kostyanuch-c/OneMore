import type { Subject } from "@/features/subjects/api/subjects";

export interface NavItemConfig {
  label: string;
  href: string;
}

export interface ProblemsDropdownProps {
  subjects: Subject[];
  isProblemsPage: boolean;
  onSelectProblemSubject: (subjectSlug: string) => void;
}

export interface MobileProblemsMenuListProps {
  subjects: Subject[];
  onCloseMenu: () => void;
}
