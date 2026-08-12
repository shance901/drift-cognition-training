import type { HTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva("inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold", {
  variants: {
    variant: {
      iris: "bg-iris-100 text-iris-700",
      ember: "bg-ember-100 text-ember-700",
      moss: "bg-moss-100 text-moss-600",
    },
  },
  defaultVariants: { variant: "iris" },
});

export interface BadgeProps extends HTMLAttributes<HTMLDivElement>, VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };
