import { useState } from "react";
import {
  Brain,
  BookOpen,
  Calendar,
  LayoutDashboard,
  ChevronLeft,
  ChevronRight,
  GraduationCap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { ModuleType } from "../TraderOSLayout";

interface SidebarProps {
  activeModule: ModuleType;
  onModuleChange: (module: ModuleType) => void;
}

const modules = [
  {
    id: "dashboard" as ModuleType,
    name: "Dashboard",
    icon: LayoutDashboard,
    description: "Overview & Analytics"
  },
  {
    id: "hypnosis" as ModuleType,
    name: "Mindset Studio",
    icon: Brain,
    description: "Focus & Discipline"
  },
  {
    id: "journal" as ModuleType,
    name: "Trade Journal",
    icon: BookOpen,
    description: "Trades, Notes, Review"
  },
  {
    id: "calendar" as ModuleType,
    name: "Economic Calendar",
    icon: Calendar,
    description: "Events & Volatility"
  },
  {
    id: "learn" as ModuleType,
    name: "Learn",
    icon: GraduationCap,
    description: "Terms, Psychology, Risk"
  }
];

export const Sidebar = ({ activeModule, onModuleChange }: SidebarProps) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "h-full bg-card border-r border-border transition-all duration-300",
        isCollapsed ? "w-16" : "w-64"
      )}
    >
      {/* Collapse Toggle */}
      <div className="p-4 border-b border-border">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="w-full justify-center"
        >
          {isCollapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Module Navigation */}
      <nav className="p-2 space-y-1">
        {modules.map((module) => {
          const Icon = module.icon;
          const isActive = activeModule === module.id;

          return (
            <Button
              key={module.id}
              variant={isActive ? "default" : "ghost"}
              className={cn(
                "w-full transition-all duration-200",
                isCollapsed ? "px-2 justify-center" : "px-3 justify-start",
                isActive && "bg-gradient-primary text-white shadow-soft"
              )}
              onClick={() => onModuleChange(module.id)}
            >
              <Icon className={cn("h-4 w-4", isCollapsed ? "" : "mr-3")} />
              {!isCollapsed && (
                <div className="flex flex-col items-start">
                  <span className="text-sm font-medium">{module.name}</span>
                  <span className="text-xs opacity-70">{module.description}</span>
                </div>
              )}
            </Button>
          );
        })}
      </nav>

    </aside>
  );
};