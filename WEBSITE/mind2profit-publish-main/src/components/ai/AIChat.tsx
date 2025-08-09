import { useState } from "react";
import { Send, Bot, User, Minimize2, Maximize2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  type: "user" | "ai";
  content: string;
  timestamp: Date;
}

export const AIChat = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "ai",
      content: "Hello! I'm your AI trading companion. I'm here to help you with strategy analysis, emotional support, journal reviews, and trading guidance. How can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState("");
  const [isMinimized, setIsMinimized] = useState(false);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");

    try {
      const res = await fetch("/api/propFirmChat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: data.reply || "Sorry, I couldn't get an answer right now.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "ai",
        content: "Sorry, there was an error contacting the AI service.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div 
      className={cn(
        "bg-card border-l border-border flex flex-col transition-all duration-300",
        isMinimized ? "w-12" : "w-80"
      )}
    >
      {/* Header */}
      <div className="p-4 border-b border-border flex items-center justify-between">
        {!isMinimized && (
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-full bg-gradient-primary flex items-center justify-center">
              <Bot className="h-4 w-4 text-white" />
            </div>
            <div>
              <h3 className="text-sm font-semibold">AI Companion</h3>
              <p className="text-xs text-success">● Online</p>
            </div>
          </div>
        )}
        
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsMinimized(!isMinimized)}
          className="h-8 w-8"
        >
          {isMinimized ? (
            <Maximize2 className="h-4 w-4" />
          ) : (
            <Minimize2 className="h-4 w-4" />
          )}
        </Button>
      </div>

      {!isMinimized && (
        <>
          {/* Messages */}
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex",
                    message.type === "user" ? "justify-end" : "justify-start"
                  )}
                >
                  <Card 
                    className={cn(
                      "max-w-[85%] p-3",
                      message.type === "user" 
                        ? "bg-gradient-primary text-white" 
                        : "bg-muted"
                    )}
                  >
                    <div className="flex items-start space-x-2">
                      {message.type === "ai" && (
                        <Bot className="h-4 w-4 mt-0.5 text-primary" />
                      )}
                      {message.type === "user" && (
                        <User className="h-4 w-4 mt-0.5" />
                      )}
                      <div className="flex-1">
                        <p className="text-sm">{message.content}</p>
                        <p className={cn(
                          "text-xs mt-1",
                          message.type === "user" ? "text-white/70" : "text-muted-foreground"
                        )}>
                          {message.timestamp.toLocaleTimeString([], {
                            hour: "2-digit",
                            minute: "2-digit"
                          })}
                        </p>
                      </div>
                    </div>
                  </Card>
                </div>
              ))}
            </div>
          </ScrollArea>

          {/* Input */}
          <div className="p-4 border-t border-border">
            <div className="flex space-x-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about trading strategies, psychology..."
                className="flex-1"
              />
              <Button 
                onClick={handleSendMessage}
                disabled={!input.trim()}
                className="bg-gradient-primary hover:bg-primary-light"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};