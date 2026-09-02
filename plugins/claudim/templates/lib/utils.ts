import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Junta classes do Tailwind resolvendo conflito. É o helper que o shadcn/ui usa. */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
