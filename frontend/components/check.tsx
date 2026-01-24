"use client";

import { useTheme } from "next-themes";
import { useEffect } from "react";

export const ThemeChecker = () => {
  const { theme, resolvedTheme } = useTheme();

  useEffect(() => {
    console.log("theme (хранится в localStorage):", theme);
    console.log("resolvedTheme (фактическая тема):", resolvedTheme);
  }, [theme, resolvedTheme]);

  return null;
};
