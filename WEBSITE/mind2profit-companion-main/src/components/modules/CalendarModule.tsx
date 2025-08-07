import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Calendar, 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  Brain,
  AlertTriangle,
  Clock,
  ExternalLink,
  Mail,
  BarChart3
} from "lucide-react";

interface EconomicEvent {
  id: string;
  title: string;
  time: string;
  impact: "low" | "medium" | "high";
  currency: string;
  actual?: string;
  forecast?: string;
  previous?: string;
  date?: string; // Add date for upcoming events
}

interface DailyData {
  date: string;
  realPnL: number;
  simulatedPnL: number;
  mindsetScore: number;
  missedOpportunities: number;
  events: EconomicEvent[];
}

export const CalendarModule = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [economicEvents, setEconomicEvents] = useState<EconomicEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // New state for upcoming events
  const [upcomingEvents, setUpcomingEvents] = useState<EconomicEvent[]>([]);
  const [upcomingLoading, setUpcomingLoading] = useState(false);
  const [upcomingError, setUpcomingError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch("http://localhost:8000/api/economic-data")
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setEconomicEvents([]);
        } else {
          setEconomicEvents([
            {
              id: data.series_id,
              title: data.title,
              time: "08:30", // US CPI usually released at 8:30am ET
              impact: "high",
              currency: "USD",
              actual: data.value,
              forecast: undefined,
              previous: undefined,
            },
          ]);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to fetch economic data");
        setEconomicEvents([]);
        setLoading(false);
      });
  }, []);

  // Fetch upcoming events from backend
  useEffect(() => {
    setUpcomingLoading(true);
    setUpcomingError(null);
    fetch("http://localhost:8000/api/economic-calendar")
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setUpcomingError(data.error);
          setUpcomingEvents([]);
        } else {
          setUpcomingEvents(data.events || []);
        }
        setUpcomingLoading(false);
      })
      .catch((err) => {
        setUpcomingError("Failed to fetch upcoming events");
        setUpcomingEvents([]);
        setUpcomingLoading(false);
      });
  }, []);

  const dailyData: DailyData[] = [
    {
      date: "2024-01-15",
      realPnL: 285,
      simulatedPnL: 340,
      mindsetScore: 8.2,
      missedOpportunities: 1,
      events: economicEvents
    },
    {
      date: "2024-01-14",
      realPnL: -95,
      simulatedPnL: 120,
      mindsetScore: 6.8,
      missedOpportunities: 3,
      events: []
    },
    {
      date: "2024-01-13",
      realPnL: 150,
      simulatedPnL: 180,
      mindsetScore: 7.5,
      missedOpportunities: 2,
      events: []
    }
  ];

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case "high": return "bg-destructive";
      case "medium": return "bg-warning";
      case "low": return "bg-success";
      default: return "bg-muted";
    }
  };

  const getImpactIcon = (impact: string) => {
    switch (impact) {
      case "high": return AlertTriangle;
      case "medium": return Clock;
      case "low": return BarChart3;
      default: return Clock;
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Economic Calendar & P&L Tracker</h1>
          <p className="text-muted-foreground">Track market events and your trading performance</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline">
            <ExternalLink className="h-4 w-4 mr-2" />
            Sync Google Calendar
          </Button>
          <Button className="bg-gradient-primary">
            <Mail className="h-4 w-4 mr-2" />
            Setup Email Alerts
          </Button>
        </div>
      </div>

      {/* Today's Summary */}
      <Card className="p-6 bg-gradient-secondary">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Today's Summary</h2>
          <Badge className="bg-warning text-warning-foreground">
            {economicEvents.length} High Impact Event{economicEvents.length !== 1 ? 's' : ''}
          </Badge>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="flex items-center space-x-3">
            <DollarSign className="h-8 w-8 text-profit" />
            <div>
              <p className="text-sm text-muted-foreground">Real P&L</p>
              <p className="text-xl font-bold text-profit">+$285</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <BarChart3 className="h-8 w-8 text-primary" />
            <div>
              <p className="text-sm text-muted-foreground">Simulated P&L</p>
              <p className="text-xl font-bold text-primary">+$340</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <Brain className="h-8 w-8 text-success" />
            <div>
              <p className="text-sm text-muted-foreground">Mindset Score</p>
              <p className="text-xl font-bold text-foreground">8.2/10</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <TrendingDown className="h-8 w-8 text-warning" />
            <div>
              <p className="text-sm text-muted-foreground">Missed Opportunities</p>
              <p className="text-xl font-bold text-foreground">1</p>
            </div>
          </div>
        </div>
      </Card>

      {/* Economic Events Today */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold">Today's Economic Events</h2>
          <Badge variant="outline">
            {loading ? 'Loading...' : error ? 'Error' : `${economicEvents.length} events`}
          </Badge>
        </div>
        {error && <div className="text-destructive mb-4">{error}</div>}
        <div className="space-y-4">
          {economicEvents.map((event) => {
            const ImpactIcon = getImpactIcon(event.impact);
            return (
              <div 
                key={event.id}
                className="flex items-center justify-between p-4 bg-muted rounded-lg hover:bg-muted/80 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-mono text-muted-foreground">{event.time}</span>
                    <Badge className={getImpactColor(event.impact)}>
                      <ImpactIcon className="h-3 w-3 mr-1" />
                      {event.impact.toUpperCase()}
                    </Badge>
                  </div>
                  
                  <div>
                    <h3 className="font-medium text-foreground">{event.title}</h3>
                    <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                      <span className="font-mono bg-background px-2 py-1 rounded">
                        {event.currency}
                      </span>
                      {event.forecast && <span>Forecast: {event.forecast}</span>}
                      {event.previous && <span>Previous: {event.previous}</span>}
                      {event.actual && <span>Actual: {event.actual}</span>}
                    </div>
                  </div>
                </div>

                {event.actual && (
                  <div className="text-right">
                    <p className="text-sm text-muted-foreground">Actual</p>
                    <p className="font-bold text-foreground">{event.actual}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </Card>

      {/* Performance Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">P&L Comparison (7 Days)</h3>
          <div className="space-y-4">
            {dailyData.map((day, index) => (
              <div key={day.date} className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  {new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
                </span>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="text-xs text-muted-foreground">Real</p>
                    <p className={`text-sm font-medium ${day.realPnL >= 0 ? 'text-profit' : 'text-loss'}`}>
                      {day.realPnL >= 0 ? '+' : ''}${day.realPnL}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-muted-foreground">Simulated</p>
                    <p className={`text-sm font-medium ${day.simulatedPnL >= 0 ? 'text-primary' : 'text-loss'}`}>
                      {day.simulatedPnL >= 0 ? '+' : ''}${day.simulatedPnL}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Weekly Insights</h3>
          <div className="space-y-4">
            <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg">
              <h4 className="font-medium text-primary mb-2">Pattern Recognition</h4>
              <p className="text-sm text-muted-foreground">
                You perform better on days with medium-impact news. Consider avoiding high-impact events.
              </p>
            </div>
            
            <div className="p-4 bg-warning/10 border border-warning/20 rounded-lg">
              <h4 className="font-medium text-warning mb-2">Missed Opportunities</h4>
              <p className="text-sm text-muted-foreground">
                Your simulated P&L is consistently higher. This suggests you're missing profitable setups.
              </p>
            </div>
            
            <div className="p-4 bg-success/10 border border-success/20 rounded-lg">
              <h4 className="font-medium text-success mb-2">Mindset Correlation</h4>
              <p className="text-sm text-muted-foreground">
                Higher mindset scores correlate with better performance. Keep focusing on psychology.
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Upcoming Events */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Upcoming High-Impact Events (7 Days)</h2>
          <Button variant="outline" size="sm">
            <Calendar className="h-4 w-4 mr-2" />
            View Full Calendar
          </Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {upcomingLoading && <div>Loading...</div>}
          {upcomingError && <div className="text-destructive mb-4">{upcomingError}</div>}
          {!upcomingLoading && !upcomingError && upcomingEvents.length === 0 && (
            <div>No upcoming high-impact events found.</div>
          )}
          {upcomingEvents.map((event) => (
            <Card key={event.id} className="p-4 bg-destructive/5 border-destructive/20">
              <div className="flex items-center justify-between mb-2">
                <Badge className="bg-destructive">HIGH</Badge>
                <span className="text-sm text-muted-foreground">{event.time}</span>
              </div>
              <h4 className="font-medium mb-1">{event.title}</h4>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">{event.date}</span>
                <span className="text-sm font-mono bg-background px-2 py-1 rounded">
                  {event.currency}
                </span>
              </div>
              <div className="flex flex-col mt-2 text-xs text-muted-foreground">
                {event.forecast && <span>Forecast: {event.forecast}</span>}
                {event.previous && <span>Previous: {event.previous}</span>}
                {event.actual && <span>Actual: {event.actual}</span>}
              </div>
            </Card>
          ))}
        </div>
      </Card>
    </div>
  );
};