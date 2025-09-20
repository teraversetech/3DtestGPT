import * as React from "react";
import { clsx } from "clsx";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost";
};

const base = "inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2";

const styles: Record<NonNullable<ButtonProps["variant"]>, string> = {
  primary: "bg-black text-white hover:bg-neutral-800 focus-visible:outline-black",
  secondary: "bg-white text-neutral-900 border border-neutral-200 hover:bg-neutral-100 focus-visible:outline-neutral-300",
  ghost: "bg-transparent text-neutral-700 hover:bg-neutral-100 focus-visible:outline-neutral-200"
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant = "primary", ...props }, ref) => (
  <button ref={ref} className={clsx(base, styles[variant], className)} {...props} />
));

Button.displayName = "Button";
