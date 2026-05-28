import type { components } from "@/shared/api/schema";

export type ProblemListItem = components["schemas"]["ProblemListItemOutSchema"];
export type Problem = components["schemas"]["ProblemOutSchema"];
export type PaginationOut = components["schemas"]["PaginationOut"];

export type SubjectProblemsResult = {
  items: Problem[];
  pagination: PaginationOut;
};
