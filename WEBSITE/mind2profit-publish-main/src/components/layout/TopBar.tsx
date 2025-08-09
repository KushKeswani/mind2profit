import { useState, useEffect } from "react";
import { Bell, Moon, Sun, Settings, Clock, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export const TopBar = () => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isDark, setIsDark] = useState(false);
  const [marketStatus, setMarketStatus] = useState<'open' | 'closed'>('closed');

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setCurrentTime(now);
      
      // Check if market is open (Monday-Friday, 9:30 AM - 4:00 PM ET)
      const dayOfWeek = now.getDay(); // 0 = Sunday, 6 = Saturday
      const hour = now.getHours();
      const minute = now.getMinutes();
      const currentTimeMinutes = hour * 60 + minute;
      
      // Market hours: 9:30 AM - 4:00 PM ET (570 - 960 minutes)
      const marketOpenMinutes = 9 * 60 + 30; // 9:30 AM
      const marketCloseMinutes = 16 * 60; // 4:00 PM
      
      const isWeekday = dayOfWeek >= 1 && dayOfWeek <= 5; // Monday to Friday
      const isMarketHours = currentTimeMinutes >= marketOpenMinutes && currentTimeMinutes < marketCloseMinutes;
      
      setMarketStatus(isWeekday && isMarketHours ? 'open' : 'closed');
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
      {/* Left: Mind2Profit Logo */}
      <div className="flex items-center space-x-3">
        <img 
          src="/logo.png" 
          alt="Mind2Profit Logo" 
          className="h-8 w-auto"
        />
        <div>
          <h1 className="text-lg font-semibold text-foreground">Mind2Profit</h1>
          <p className="text-xs text-muted-foreground">AI Trading Companion</p>
        </div>
      </div>

      {/* Center: Date and Time */}
      <div className="flex items-center space-x-6">
        <div className="text-center">
          <div className="text-lg font-mono font-semibold text-foreground">
            {formatTime(currentTime)}
          </div>
          <div className="text-xs text-muted-foreground">
            {formatDate(currentTime)}
          </div>
          <div className="flex items-center justify-center gap-1 mt-1">
            <Clock className="h-3 w-3" />
            <span className={`text-xs font-medium ${
              marketStatus === 'open' ? 'text-green-600' : 'text-red-600'
            }`}>
              Market {marketStatus === 'open' ? 'OPEN' : 'CLOSED'}
            </span>
          </div>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center space-x-3">
        {/* Notifications */}
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-4 w-4" />
          <Badge className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 text-xs bg-primary">
            3
          </Badge>
        </Button>

        {/* Theme Toggle */}
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          className="transition-all duration-300"
        >
          {isDark ? (
            <Sun className="h-4 w-4" />
          ) : (
            <Moon className="h-4 w-4" />
          )}
        </Button>

        {/* Settings */}
        <Button variant="ghost" size="icon">
          <Settings className="h-4 w-4" />
        </Button>

        {/* Logout */}
        <Button 
          variant="ghost" 
          size="icon"
          onClick={() => {
            logout();
            navigate('/');
          }}
          title="Logout"
        >
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
};