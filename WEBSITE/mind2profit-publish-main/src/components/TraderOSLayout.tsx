import { useState } from "react";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Sidebar } from "./sidebar/Sidebar";
import { TopBar } from "./layout/TopBar";
import { MainContent } from "./layout/MainContent";

export type ModuleType = 
  | "dashboard" 
  | "hypnosis" 
  | "journal" 
  | "calendar"
  | "learn";

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
          <MainContent activeModule={activeModule} />
        </div>
      </div>
    </SidebarProvider>
  );
};

export default Mind2ProfitLayout;