type ChipColor =
  | "default"
  | "primary"
  | "secondary"
  | "success"
  | "warning"
  | "danger";

export function getDifficultyColor(value: string): ChipColor {
  if (value === "easy") return "success";
  if (value === "medium") return "warning";
  if (value === "hard") return "danger";

  return "default";
}
