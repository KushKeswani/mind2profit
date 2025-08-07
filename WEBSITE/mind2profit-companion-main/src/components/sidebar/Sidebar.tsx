import { useState } from "react";
import { 
  Brain, 
  TrendingUp, 
  Bot, 
  Users, 
  BookOpen, 
  Calendar,
  LayoutDashboard,
  ChevronLeft,
  ChevronRight
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
    name: "Hypnosis Studio",
    icon: Brain,
    description: "Mindset & Psychology"
  },
  {
    id: "strategies" as ModuleType,
    name: "Strategies",
    icon: TrendingUp,
    description: "Profitable Trading Plans"
  },
  {
    id: "automation" as ModuleType,
    name: "Automation Lab",
    icon: Bot,
    description: "Trading Bots & Logic"
  },
  {
    id: "partner" as ModuleType,
    name: "Virtual Partner",
    icon: Users,
    description: "Daily Check-ins"
  },
  {
    id: "journal" as ModuleType,
    name: "Trade Journal",
    icon: BookOpen,
    description: "Reflect & Learn"
  },
  {
    id: "calendar" as ModuleType,
    name: "Economic Calendar",
    icon: Calendar,
    description: "Events & P&L Tracking"
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