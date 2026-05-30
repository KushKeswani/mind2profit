import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { loadAppState, saveAppState } from "@/lib/storage";
import { seedDefaultScriptsIfNeeded } from "@/lib/seedScripts";
import type { Script, ScriptVariant } from "@/lib/types";
import { Play, Pause, Plus, Trash2, Save } from "lucide-react";

const VARIANT_LABELS: Record<ScriptVariant, string> = {
  pre_market: "Pre-Market",
  after_loss: "After Loss",
  fomo_overtrade: "FOMO/Overtrade",
  confidence: "Confidence",
};

export default function ScriptsPage() {
  const [appState, setAppState] = useState(loadAppState());
  const [editingScript, setEditingScript] = useState<Script | null>(null);
  const [audioPlaying, setAudioPlaying] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    seedDefaultScriptsIfNeeded();
    setAppState(loadAppState());
  }, []);

  const handleEdit = (script: Script) => {
    setEditingScript({ ...script });
  };

  const handleSave = () => {
    if (!editingScript) return;

    const state = loadAppState();
    const index = state.scripts.findIndex((s) => s.id === editingScript.id);
    if (index >= 0) {
      state.scripts[index] = editingScript;
    }
    saveAppState(state);
    setAppState(state);
    setEditingScript(null);
  };

  const handleAddLine = () => {
    if (!editingScript) return;
    setEditingScript({
      ...editingScript,
      lines: [...editingScript.lines, ""],
    });
  };

  const handleRemoveLine = (index: number) => {
    if (!editingScript || editingScript.lines.length <= 1) return;
    setEditingScript({
      ...editingScript,
      lines: editingScript.lines.filter((_, i) => i !== index),
    });
  };

  const handleLineChange = (index: number, value: string) => {
    if (!editingScript) return;
    const newLines = [...editingScript.lines];
    newLines[index] = value;
    setEditingScript({
      ...editingScript,
      lines: newLines,
    });
  };

  const handlePlayAudio = (script: Script) => {
    if (!script.audioUrl) return;

    if (audioPlaying === script.id) {
      if (audioRef.current) {
        audioRef.current.pause();
        setAudioPlaying(null);
      }
    } else {
      if (audioRef.current) {
        audioRef.current.src = script.audioUrl;
        audioRef.current.play();
        setAudioPlaying(script.id);
      }
    }
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold mb-2">Scripts</h1>
          <p className="text-muted-foreground">Manage your trading psychology scripts.</p>
        </div>

        <div className="space-y-4">
          {appState.scripts.map((script) => (
            <Card key={script.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <CardTitle>{script.title}</CardTitle>
                    <Badge variant="outline">{VARIANT_LABELS[script.variant]}</Badge>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleEdit(script)}
                  >
                    Edit
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                {editingScript?.id === script.id ? (
                  <div className="space-y-4">
                    <div>
                      <label className="text-sm font-medium block mb-2">Title</label>
                      <Input
                        value={editingScript.title}
                        onChange={(e) =>
                          setEditingScript({ ...editingScript, title: e.target.value })
                        }
                      />
                    </div>

                    <div>
                      <label className="text-sm font-medium block mb-2">Lines</label>
                      <div className="space-y-2">
                        {editingScript.lines.map((line, idx) => (
                          <div key={idx} className="flex gap-2">
                            <Textarea
                              value={line}
                              onChange={(e) => handleLineChange(idx, e.target.value)}
                              rows={2}
                              className="flex-1"
                            />
                            <Button
                              variant="outline"
                              size="icon"
                              onClick={() => handleRemoveLine(idx)}
                              disabled={editingScript.lines.length <= 1}
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        ))}
                        <Button variant="outline" onClick={handleAddLine} size="sm">
                          <Plus className="h-4 w-4 mr-2" />
                          Add Line
                        </Button>
                      </div>
                    </div>

                    <div>
                      <label className="text-sm font-medium block mb-2">Audio URL (optional)</label>
                      <Input
                        type="url"
                        value={editingScript.audioUrl || ""}
                        onChange={(e) =>
                          setEditingScript({
                            ...editingScript,
                            audioUrl: e.target.value || undefined,
                          })
                        }
                        placeholder="https://example.com/audio.mp3"
                      />
                    </div>

                    <div className="flex gap-2">
                      <Button onClick={handleSave}>
                        <Save className="h-4 w-4 mr-2" />
                        Save
                      </Button>
                      <Button
                        variant="outline"
                        onClick={() => setEditingScript(null)}
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      {script.lines.map((line, idx) => (
                        <p key={idx} className="text-sm">
                          {line}
                        </p>
                      ))}
                    </div>

                    {script.audioUrl && (
                      <div>
                        <audio
                          ref={audioRef}
                          onEnded={() => setAudioPlaying(null)}
                          onPause={() => setAudioPlaying(null)}
                        />
                        <Button
                          variant="outline"
                          onClick={() => handlePlayAudio(script)}
                        >
                          {audioPlaying === script.id ? (
                            <>
                              <Pause className="h-4 w-4 mr-2" />
                              Pause
                            </>
                          ) : (
                            <>
                              <Play className="h-4 w-4 mr-2" />
                              Play Audio
                            </>
                          )}
                        </Button>
                      </div>
                    )}

                    {!script.audioUrl && (
                      <p className="text-sm text-muted-foreground">No audio URL set</p>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

