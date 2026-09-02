/* Primitivo do shadcn/ui. Os outros vêm com `npx shadcn@latest add <nome>`
   e caem nesta mesma pasta. Editar aqui é permitido — o código é seu. */

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const botao = cva(
  "inline-flex items-center justify-center gap-2 rounded-padrao text-sm font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-marca",
  {
    variants: {
      variant: {
        default: "bg-marca text-white hover:opacity-90",
        outline: "border border-borda bg-superficie hover:bg-marca-suave",
        ghost: "hover:bg-marca-suave",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3",
        lg: "h-10 px-6",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof botao>;

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => (
    <button ref={ref} className={cn(botao({ variant, size, className }))} {...props} />
  ),
);
Button.displayName = "Button";
