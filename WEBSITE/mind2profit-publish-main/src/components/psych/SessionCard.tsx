import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { LiveSession } from "@/lib/types";
import { format } from "date-fns";

interface SessionCardProps {
  session: LiveSession;
  onClick?: () => void;
}

export function SessionCard({ session, onClick }: SessionCardProps) {
  const date = new Date(session.startedAt);
  const violationsCount = session.violations.length;
  const followedPlan = session.reflection?.followedPlan;

  return (
    <Card
      className={onClick ? "cursor-pointer hover:shadow-md transition-shadow" : ""}
      onClick={onClick}
    >
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg">
            {format(date, "MMM d, yyyy")} at {format(date, "h:mm a")}
          </CardTitle>
          <Badge
            variant={
              session.state === "completed" && followedPlan
                ? "default"
                : session.state === "stopped"
                ? "destructive"
                : "secondary"
            }
          >
            {session.state}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex flex-wrap gap-2 text-sm">
          <Badge variant="outline">Intent: {session.intent}</Badge>
          <Badge variant="outline">Emotion: {session.emotionStart}</Badge>
          <Badge variant={session.gatePassed ? "default" : "destructive"}>
            Gate: {session.gatePassed ? "Passed" : "Failed"}
          </Badge>
        </div>
        <div className="text-sm text-muted-foreground">
          Violations: {violationsCount}
        </div>
        {session.reflection && (
          <div className="text-sm">
            Followed plan:{" "}
            <span className={followedPlan ? "text-success" : "text-destructive"}>
              {followedPlan ? "Yes" : "No"}
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}


