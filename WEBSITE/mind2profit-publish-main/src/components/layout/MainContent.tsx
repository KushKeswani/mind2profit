import { DashboardModule } from "../modules/DashboardModule";
import { HypnosisModule } from "../modules/HypnosisModule";
import { JournalModule } from "../modules/JournalModule";
import { CalendarModule } from "../modules/CalendarModule";
import { LearnModule } from "../modules/LearnModule";
import { Alert, AlertDescription } from "@/components/ui/alert";
import type { ModuleType } from "../TraderOSLayout";

interface MainContentProps {
  activeModule: ModuleType;
}

export const MainContent = ({ activeModule }: MainContentProps) => {
  const renderModule = () => {
    try {
      switch (activeModule) {
        case "dashboard":
          return <DashboardModule />;
        case "hypnosis":
          return <HypnosisModule />;
        case "journal":
          return <JournalModule />;
        case "calendar":
          return <CalendarModule />;
        case "learn":
          return <LearnModule />;
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