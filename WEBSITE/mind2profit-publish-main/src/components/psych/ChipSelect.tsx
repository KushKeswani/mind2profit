import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface ChipSelectProps<T extends string> {
  options: { value: T; label: string }[];
  value: T | undefined;
  onChange: (value: T) => void;
  className?: string;
}

export function ChipSelect<T extends string>({
  options,
  value,
  onChange,
  className,
}: ChipSelectProps<T>) {
  return (
    <div className={cn("flex flex-wrap gap-2", className)}>
      {options.map((option) => (
        <Button
          key={option.value}
          type="button"
          variant={value === option.value ? "default" : "outline"}
          onClick={() => onChange(option.value)}
          className={cn(
            "rounded-full",
            value === option.value && "bg-primary text-primary-foreground"
          )}
        >
          {option.label}
        </Button>
      ))}
    </div>
  );
}


