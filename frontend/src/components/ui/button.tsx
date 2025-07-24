import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-semibold transition-all duration-200 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:ring-2 focus-visible:ring-offset-2 transform active:scale-95",
  {
    variants: {
      variant: {
        default:
          "bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-medium hover:from-primary-600 hover:to-primary-700 hover:shadow-hard focus-visible:ring-primary-500 hover:-translate-y-0.5",
        secondary:
          "bg-gradient-to-r from-secondary-500 to-secondary-600 text-white shadow-medium hover:from-secondary-600 hover:to-secondary-700 hover:shadow-hard focus-visible:ring-secondary-500 hover:-translate-y-0.5",
        accent:
          "bg-gradient-to-r from-accent-500 to-accent-600 text-white shadow-medium hover:from-accent-600 hover:to-accent-700 hover:shadow-hard focus-visible:ring-accent-500 hover:-translate-y-0.5",
        outline:
          "border-2 border-primary-200 bg-white/80 backdrop-blur-sm text-primary-700 shadow-soft hover:bg-primary-50 hover:border-primary-300 hover:shadow-medium focus-visible:ring-primary-500 hover:-translate-y-0.5",
        ghost:
          "text-neutral-700 hover:bg-neutral-100 hover:text-neutral-900 focus-visible:ring-neutral-500",
        destructive:
          "bg-gradient-to-r from-error-500 to-error-600 text-white shadow-medium hover:from-error-600 hover:to-error-700 hover:shadow-hard focus-visible:ring-error-500 hover:-translate-y-0.5",
        success:
          "bg-gradient-to-r from-success-500 to-success-600 text-white shadow-medium hover:from-success-600 hover:to-success-700 hover:shadow-hard focus-visible:ring-success-500 hover:-translate-y-0.5",
        glow:
          "bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-glow hover:shadow-glow-purple focus-visible:ring-primary-500 hover:-translate-y-0.5 animate-pulse",
        link: "text-primary-600 underline-offset-4 hover:underline hover:text-primary-700",
      },
      size: {
        sm: "h-8 px-3 py-1.5 text-xs rounded-lg has-[>svg]:px-2",
        default: "h-10 px-6 py-2.5 has-[>svg]:px-4",
        lg: "h-12 px-8 py-3 text-base has-[>svg]:px-6",
        xl: "h-14 px-10 py-4 text-lg has-[>svg]:px-8",
        icon: "size-10 p-0",
        "icon-sm": "size-8 p-0",
        "icon-lg": "size-12 p-0",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<"button"> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean
  }) {
  const Comp = asChild ? Slot : "button"

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

export { Button, buttonVariants }
