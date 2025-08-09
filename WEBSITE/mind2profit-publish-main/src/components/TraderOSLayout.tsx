import { useState } from "react";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Sidebar } from "./sidebar/Sidebar";
import { TopBar } from "./layout/TopBar";
import { MainContent } from "./layout/MainContent";
import { AIChat } from "./ai/AIChat";

export type ModuleType = 
  | "dashboard" 
  | "hypnosis" 
  | "strategies" 
  | "strategy-results"
  | "automation" 
  | "partner" 
  | "journal" 
  | "calendar";

const Mind2ProfitLayout = () => {
  const [activeModule, setActiveModule] = useState<ModuleType>("dashboard");

  return (
    <SidebarProvider>
      <div className="min-h-screen w-full bg-background flex flex-col">
        {/* Top Bar */}
        <TopBar />

        {/* Main Layout */}
        <div className="flex flex-1 overflow-hidden">
          {/* Left Sidebar */}
          <Sidebar 
            activeModule={activeModule} 
            onModuleChange={setActiveModule} 
          />

          {/* Main Content */}
          <MainContent activeModule={activeModule} onModuleChange={setActiveModule} />
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Mind2ProfitLayout;