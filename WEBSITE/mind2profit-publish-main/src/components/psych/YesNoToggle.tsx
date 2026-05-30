import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface YesNoToggleProps {
  value: boolean | undefined;
  onChange: (value: boolean) => void;
  label: string;
  className?: string;
}

export function YesNoToggle({ value, onChange, label, className }: YesNoToggleProps) {
  return (
    <div className={cn("space-y-2", className)}>
      <label className="text-sm font-medium block">{label}</label>
      <div className="flex gap-2">
        <Button
          type="button"
          variant={value === true ? "default" : "outline"}
          onClick={() => onChange(true)}
          className={cn(
            "flex-1",
            value === true && "bg-primary text-primary-foreground"
          )}
        >
          Yes
        </Button>
        <Button
          type="button"
          variant={value === false ? "default" : "outline"}
          onClick={() => onChange(false)}
          className={cn(
            "flex-1",
            value === false && "bg-destructive text-destructive-foreground"
          )}
        >
          No
        </Button>
      </div>
    </div>
  );
}


