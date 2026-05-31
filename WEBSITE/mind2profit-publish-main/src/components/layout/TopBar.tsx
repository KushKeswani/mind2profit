import { useState, useEffect } from "react";
import { Bell, Moon, Sun, Settings, Clock, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate, Link } from "react-router-dom";
import { useNotifications } from "@/contexts/NotificationContext";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";

export const TopBar = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const { items, unreadCount, markRead, markAllRead } = useNotifications();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isDark, setIsDark] = useState(false);
  const [marketStatus, setMarketStatus] = useState<"open" | "closed">("closed");
  const [notifOpen, setNotifOpen] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setCurrentTime(now);

      const dayOfWeek = now.getDay();
      const hour = now.getHours();
      const minute = now.getMinutes();
      const currentTimeMinutes = hour * 60 + minute;

      const marketOpenMinutes = 9 * 60 + 30;
      const marketCloseMinutes = 16 * 60;

      const isWeekday = dayOfWeek >= 1 && dayOfWeek <= 5;
      const isMarketHours = currentTimeMinutes >= marketOpenMinutes && currentTimeMinutes < marketCloseMinutes;

      setMarketStatus(isWeekday && isMarketHours ? "open" : "closed");
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const toggleTheme = () => {
    setIsDark(!isDark);
    document.documentElement.classList.toggle("dark");
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("en-US", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <header className="h-14 border-b border-border bg-card/50 backdrop-blur-sm px-6 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <img src="/logo.png" alt="Mind2Profit Logo" className="h-8 w-auto" />
        <div>
          <h1 className="text-lg font-semibold text-foreground">Mind2Profit</h1>
          <p className="text-xs text-muted-foreground">AI Trading Companion</p>
        </div>
      </div>

      <div className="flex items-center space-x-6">
        <div className="text-center">
          <div className="text-lg font-mono font-semibold text-foreground">{formatTime(currentTime)}</div>
          <div className="text-xs text-muted-foreground">{formatDate(currentTime)}</div>
          <div className="flex items-center justify-center gap-1 mt-1">
            <Clock className="h-3 w-3" />
            <span
              className={`text-xs font-medium ${
                marketStatus === "open" ? "text-green-600" : "text-red-600"
              }`}
            >
              Market {marketStatus === "open" ? "OPEN" : "CLOSED"}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <Popover open={notifOpen} onOpenChange={setNotifOpen}>
          <PopoverTrigger asChild>
            <Button variant="ghost" size="icon" className="relative" aria-label="Notifications">
              <Bell className="h-4 w-4" />
              {unreadCount > 0 && (
                <Badge className="absolute -top-1 -right-1 h-5 min-w-5 justify-center rounded-full p-0 px-1 text-xs leading-none bg-primary">
                  {unreadCount > 99 ? "99+" : unreadCount}
                </Badge>
              )}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-96 p-0" align="end">
            <div className="flex items-center justify-between border-b px-3 py-2">
              <span className="text-sm font-medium">Notifications</span>
              {items.length > 0 && (
                <Button variant="ghost" size="sm" className="h-7 text-xs" onClick={() => markAllRead()}>
                  Mark all read
                </Button>
              )}
            </div>
            <ScrollArea className="h-[min(70vh,360px)]">
              {items.length === 0 ? (
                <p className="p-4 text-sm text-muted-foreground">You&apos;re all caught up. EOD P&L and journal reminders will show here.</p>
              ) : (
                <ul className="divide-y">
                  {items.map((n) => (
                    <li key={n.id}>
                      <button
                        type="button"
                        className={cn(
                          "w-full text-left p-3 text-sm transition-colors hover:bg-muted/80",
                          !n.read && "bg-primary/5"
                        )}
                        onClick={() => {
                          markRead(n.id);
                        }}
                      >
                        <p className="font-medium text-foreground">{n.title}</p>
                        <p className="text-muted-foreground mt-0.5 line-clamp-3">{n.body}</p>
                        <p className="text-xs text-muted-foreground mt-1">
                          {new Date(n.createdAt).toLocaleString()}
                        </p>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </ScrollArea>
            <div className="border-t px-3 py-2 text-xs text-muted-foreground">
              Signed in as {user?.email}
            </div>
          </PopoverContent>
        </Popover>

        <Button variant="ghost" size="icon" onClick={toggleTheme} className="transition-all duration-300" type="button">
          {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </Button>

        <Button variant="ghost" size="icon" asChild title="Settings">
          <Link to="/settings">
            <Settings className="h-4 w-4" />
          </Link>
        </Button>

        <Button
          variant="ghost"
          size="icon"
          onClick={() => {
            logout();
            navigate("/");
          }}
          title="Logout"
        >
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
};
