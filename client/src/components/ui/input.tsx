import { forwardRef, type InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type, ...props }, ref) => (
    <input
      type={type}
      ref={ref}
      className={cn(
        "flex h-11 w-full rounded-xl border border-border bg-surface px-4 text-[15px] text-ink placeholder:text-ink-soft transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-iris-500 disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";

export { Input };
