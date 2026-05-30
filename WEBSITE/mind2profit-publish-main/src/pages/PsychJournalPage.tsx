import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { SessionCard } from "@/components/psych/SessionCard";
import { loadAppState, updateSession } from "@/lib/storage";
import type { LiveSession, Reflection } from "@/lib/types";
import { format } from "date-fns";

export default function PsychJournalPage() {
  const [appState, setAppState] = useState(loadAppState());
  const [selectedSession, setSelectedSession] = useState<LiveSession | null>(null);
  const [showDetail, setShowDetail] = useState(false);
  const [editingReflection, setEditingReflection] = useState(false);
  const [reflectionNote, setReflectionNote] = useState("");

  useEffect(() => {
    setAppState(loadAppState());
  }, []);

  const sessions = [...appState.sessions].sort((a, b) => b.startedAt - a.startedAt);

  const handleSessionClick = (session: LiveSession) => {
    setSelectedSession(session);
    setReflectionNote(session.reflection?.note || "");
    setShowDetail(true);
  };

  const handleSaveReflectionNote = () => {
    if (!selectedSession) return;

    const updated: LiveSession = {
      ...selectedSession,
      reflection: {
        ...selectedSession.reflection!,
        note: reflectionNote,
      } as Reflection,
    };

    updateSession(updated);
    setAppState(loadAppState());
    setEditingReflection(false);
    setSelectedSession(updated);
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Trading Journal</h1>
          <p className="text-muted-foreground">Review your trading sessions and reflections.</p>
        </div>

        <div className="space-y-4">
          {sessions.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center text-muted-foreground">
                No sessions yet. Start a live trading session to begin logging.
              </CardContent>
            </Card>
          ) : (
            sessions.map((session) => (
              <SessionCard
                key={session.id}
                session={session}
                onClick={() => handleSessionClick(session)}
              />
            ))
          )}
        </div>

        {/* Session Detail Dialog */}
        <Dialog open={showDetail} onOpenChange={setShowDetail}>
          <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
            {selectedSession && (
              <>
                <DialogHeader>
                  <DialogTitle>
                    Session: {format(new Date(selectedSession.startedAt), "MMM d, yyyy 'at' h:mm a")}
                  </DialogTitle>
                </DialogHeader>

                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold mb-2">Details</h3>
                    <div className="space-y-1 text-sm">
                      <p>
                        <span className="text-muted-foreground">State:</span> {selectedSession.state}
                      </p>
                      <p>
                        <span className="text-muted-foreground">Intent:</span> {selectedSession.intent}
                      </p>
                      <p>
                        <span className="text-muted-foreground">Starting Emotion:</span>{" "}
                        {selectedSession.emotionStart}
                      </p>
                      <p>
                        <span className="text-muted-foreground">Script Used:</span>{" "}
                        {selectedSession.variantUsed}
                      </p>
                      <p>
                        <span className="text-muted-foreground">Gate Passed:</span>{" "}
                        {selectedSession.gatePassed ? "Yes" : "No"}
                      </p>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-semibold mb-2">Gate Answers</h3>
                    <div className="space-y-1 text-sm">
                      <p>
                        Defined Setup: {selectedSession.gateAnswers.defined_setup ? "Yes" : "No"}
                      </p>
                      <p>
                        Know Stop: {selectedSession.gateAnswers.know_stop ? "Yes" : "No"}
                      </p>
                      <p>
                        OK No Trade: {selectedSession.gateAnswers.ok_no_trade ? "Yes" : "No"}
                      </p>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-semibold mb-2">
                      Violations ({selectedSession.violations.length})
                    </h3>
                    {selectedSession.violations.length === 0 ? (
                      <p className="text-sm text-muted-foreground">No violations</p>
                    ) : (
                      <div className="space-y-2">
                        {selectedSession.violations.map((violation) => (
                          <Card key={violation.id}>
                            <CardContent className="p-3">
                              <div className="text-sm">
                                <p className="font-medium">{violation.type}</p>
                                <p className="text-muted-foreground">
                                  {format(new Date(violation.ts), "h:mm a")}
                                </p>
                                {violation.note && (
                                  <p className="text-muted-foreground mt-1">{violation.note}</p>
                                )}
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    )}
                  </div>

                  <div>
                    <h3 className="font-semibold mb-2">
                      Check-Ins ({selectedSession.checkIns.length})
                    </h3>
                    {selectedSession.checkIns.length === 0 ? (
                      <p className="text-sm text-muted-foreground">No check-ins</p>
                    ) : (
                      <div className="space-y-2">
                        {selectedSession.checkIns.map((checkIn) => (
                          <Card key={checkIn.id}>
                            <CardContent className="p-3">
                              <div className="text-sm">
                                <p>
                                  Was this planned? {checkIn.answer ? "Yes" : "No"}
                                </p>
                                <p className="text-muted-foreground">
                                  {format(new Date(checkIn.ts), "h:mm a")}
                                </p>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    )}
                  </div>

                  {selectedSession.reflection && (
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-semibold">Reflection</h3>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => setEditingReflection(!editingReflection)}
                        >
                          {editingReflection ? "Cancel" : "Edit"}
                        </Button>
                      </div>
                      {editingReflection ? (
                        <div className="space-y-2">
                          <Textarea
                            value={reflectionNote}
                            onChange={(e) => setReflectionNote(e.target.value)}
                            rows={4}
                          />
                          <Button onClick={handleSaveReflectionNote} size="sm">
                            Save
                          </Button>
                        </div>
                      ) : (
                        <div className="space-y-2 text-sm">
                          <p>
                            Followed Plan:{" "}
                            <span
                              className={
                                selectedSession.reflection.followedPlan
                                  ? "text-success"
                                  : "text-destructive"
                              }
                            >
                              {selectedSession.reflection.followedPlan ? "Yes" : "No"}
                            </span>
                          </p>
                          <p>
                            Emotion During: {selectedSession.reflection.emotionDuring}
                          </p>
                          {selectedSession.reflection.note && (
                            <p className="text-muted-foreground">
                              {selectedSession.reflection.note}
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}


