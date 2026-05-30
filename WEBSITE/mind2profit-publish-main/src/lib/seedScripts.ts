import type { Script } from "./types";
import { loadAppState, saveAppState } from "./storage";

export function seedDefaultScriptsIfNeeded(): void {
  const state = loadAppState();
  if (state.scripts.length > 0) {
    return; // Already has scripts
  }

  const defaultScripts: Script[] = [
    {
      id: "pre_market_default",
      variant: "pre_market",
      title: "Pre-Market Preparation",
      lines: [
        "I am clear and focused.",
        "I will only trade my defined setups.",
        "I know exactly where I exit if I'm wrong.",
        "I am okay with taking zero trades today.",
        "If it's not clear, I stay flat.",
      ],
      audioUrl: undefined,
    },
    {
      id: "after_loss_default",
      variant: "after_loss",
      title: "After Loss Reset",
      lines: [
        "That loss is over. It cannot be undone.",
        "Revenge trading is not trading. It is gambling.",
        "I step back. I breathe.",
        "I will not trade again until I am calm.",
        "Walking away after a loss is a winning decision.",
      ],
      audioUrl: undefined,
    },
    {
      id: "fomo_overtrade_default",
      variant: "fomo_overtrade",
      title: "FOMO & Overtrade Check",
      lines: [
        "I am feeling the urge to trade right now.",
        "Is this one of my defined setups?",
        "Am I following the plan I confirmed earlier?",
        "If no, then this is emotional trading.",
        "I pause. I wait. I stay disciplined.",
      ],
      audioUrl: undefined,
    },
    {
      id: "confidence_default",
      variant: "confidence",
      title: "Confidence Reinforcement",
      lines: [
        "I have a plan. I know my setups.",
        "I trust my process, not the outcome.",
        "One trade does not define me.",
        "I am disciplined. I am patient.",
        "I trade the plan, not the emotion.",
      ],
      audioUrl: undefined,
    },
  ];

  state.scripts = defaultScripts;
  saveAppState(state);
}


