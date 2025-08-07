import { useState } from "react";
import { DashboardModule } from "../modules/DashboardModule";
import { HypnosisModule } from "../modules/HypnosisModule";
import { StrategiesModule } from "../modules/StrategiesModule";
import { StrategyResultsPage } from "../modules/StrategyResultsPage";
import { AutomationModule } from "../modules/AutomationModule";
import { PartnerModule } from "../modules/PartnerModule";
import { JournalModule } from "../modules/JournalModule";
import { CalendarModule } from "../modules/CalendarModule";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { ModuleType } from "../TraderOSLayout";

interface MainContentProps {
  activeModule: ModuleType;
  onModuleChange?: (module: ModuleType) => void;
}

export const MainContent = ({ activeModule, onModuleChange }: MainContentProps) => {
  const [strategyData, setStrategyData] = useState<any>(null);

  const renderModule = () => {
    try {
      switch (activeModule) {
        case "dashboard":
          return <DashboardModule />;
        case "hypnosis":
          return <HypnosisModule />;
        case "strategies":
          return <StrategiesModule onNavigateToResults={(data) => {
            console.log('📊 MainContent received strategy data:', data);
            console.log('🔄 Setting strategy data and changing module...');
            setStrategyData(data);
            onModuleChange?.("strategy-results");
            console.log('✅ Module change completed');
          }} />;
        case "strategy-results":
          console.log('📊 Rendering StrategyResultsPage with strategyData:', strategyData);
          return <StrategyResultsPage 
            strategyData={strategyData}
            onBackToStrategies={() => onModuleChange?.("strategies")} 
          />;
        case "automation":
          return <AutomationModule />;
        case "partner":
          return <PartnerModule />;
        case "journal":
          return <JournalModule />;
        case "calendar":
          return <CalendarModule />;
        default:
          return <DashboardModule />;
      }
    } catch (error) {
      console.error('❌ Error rendering module:', error);
      return (
        <div className="space-y-6">
          <h1 className="text-2xl font-bold">Error</h1>
          <Alert>
            <AlertDescription>
              An error occurred while rendering the module. Please check the console for details.
            </AlertDescription>
          </Alert>
        </div>
      );
    }
  };

  return (
    <main className="flex-1 overflow-auto bg-background-secondary">
      <div className="p-6 h-full">
        {renderModule()}
      </div>
    </main>
  );
};