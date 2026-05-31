# Trading Psychology System

A behavior-control and accountability system for traders, built to help maintain discipline through structured gating, check-ins, and reflection.

## Overview

The system funnels all trading activity through a central "Live Trading" hub (`/live`). Users must complete a mandatory gating process before entering "Live Mode", which includes:

1. Reading/listening to a psychology script
2. Declaring trading intent
3. Acknowledging starting emotion
4. Passing a plan verification gate
5. Final external conscience confirmation

During Live Mode, users can log trades, perform check-ins, and access an emergency stop button. After stopping, a 15-second reflection is required.

## Pages

- **`/live`** - Live Trading Hub (primary entry point)
- **`/journal`** - Trading journal with session history and details
- **`/scripts`** - Script manager for editing psychology scripts
- **`/stats`** - Discipline score and streaks dashboard
- **`/learn`** - Short psychology lessons

## Data Storage

All data is stored in `localStorage` under the key `psych_app_state_v1`. The data structure includes:

- Scripts (4 variants: pre_market, after_loss, fomo_overtrade, confidence)
- Live sessions (with gate answers, violations, check-ins, reflections)
- Current session ID
- Streaks (planFollowedDays, noRevengeDays, acceptedNoTradeDays, bestPlanFollowedDays)
- Lockout status (after using STOP TRADING)

## Key Flows

### Starting a Trading Session

1. User clicks "START TRADING" on `/live`
2. Gating modal opens with 5 steps:
   - **Script**: Read/listen to script (minimum 20 seconds)
   - **Intent**: Declare bias (Longs/Shorts/Waiting/Not Sure)
   - **Emotion**: Select starting emotion
   - **Gate**: Answer 3 verification questions
   - **External Conscience**: Final confirmation
3. If gate passes → Enter Live Mode
4. If gate fails → Options: Replay Script, Switch to SIM, Stay Flat (logs violation)

### Live Mode

- Persistent status bar showing: LIVE badge, intent, emotion, script used, timer
- Actions:
  - **Log Trade**: Triggers check-in ("Was this planned?")
  - **Manual Check-In**: Same check-in without logging trade
  - **STOP TRADING**: Immediately stops session, locks trading for the day

### Check-Ins

When user logs a trade or triggers manual check-in:
- Question: "Was this trade part of the plan you confirmed?"
- If "No": Logs `off_plan_trade` violation
- Option to play reset audio

### Stop Trading Flow

1. User clicks "STOP TRADING"
2. Session state → "stopped"
3. Trading locked for remainder of day (stored in localStorage)
4. Reset audio plays if available
5. Reflection modal opens (15-second minimum)

### Reflection

After stopping a session:
- Followed plan? (Yes/No)
- Emotion during session? (select from chips)
- Optional note
- Updates streaks and completes session

## Discipline Score Calculation

Calculated for the last 7 days:
- Start at 100
- -10 per `off_plan_trade` violation
- -15 per `revenge` violation
- -5 per `gate_failed_trade_attempt` violation
- Capped at 0-100

## Streaks

- **planFollowedDays**: Increments when reflection.followedPlan = true
- **noRevengeDays**: Increments when no revenge violations that day
- **acceptedNoTradeDays**: Increments when intent=waiting or "Stay Flat" used
- **bestPlanFollowedDays**: Tracks highest planFollowedDays streak

## Default Scripts

Four default scripts are seeded on first load:

1. **Pre-Market**: Preparation script
2. **After Loss**: Reset script
3. **FOMO/Overtrade**: Urge management script
4. **Confidence**: Reinforcement script

Scripts can be edited in `/scripts` with:
- Title
- Lines (add/remove text lines)
- Audio URL (optional)

## Extending the System

### Adding Backend Integration

To add backend support:

1. Replace `loadAppState()` and `saveAppState()` in `/lib/storage.ts` with API calls
2. Add authentication context
3. Store scripts and sessions in database
4. Add real-time sync if needed

### Adding Audio Support

Scripts support optional `audioUrl`. To enable audio:

1. Host audio files
2. Add URLs to scripts via `/scripts` page
3. Audio will play in gating flow and live mode

### Adding New Violation Types

1. Update `Violation.type` in `/lib/types.ts`
2. Update discipline score calculation in `/pages/PsychStatsPage.tsx`
3. Add UI for logging new violation types in live mode

### Adding New Script Variants

1. Update `ScriptVariant` type in `/lib/types.ts`
2. Add variant label in `VARIANT_LABELS` in `/pages/ScriptsPage.tsx`
3. Add default script in `/lib/seedScripts.ts`

## File Structure

```
src/
  lib/
    types.ts          - TypeScript types
    storage.ts        - localStorage operations
    seedScripts.ts    - Default script seeding
  components/
    psych/
      ChipSelect.tsx      - Chip selection component
      YesNoToggle.tsx     - Yes/No toggle component
      SessionCard.tsx     - Session card for journal
      Stepper.tsx         - Wizard stepper component
  pages/
    LiveTradingPage.tsx   - Main live trading hub
    PsychJournalPage.tsx  - Journal view
    ScriptsPage.tsx       - Script manager
    PsychStatsPage.tsx    - Stats dashboard
    LearnPage.tsx         - Psychology lessons
```

## Development Notes

- All components use existing shadcn/ui components
- Mobile-responsive design
- No emojis (per requirements)
- Blunt but not insulting wording
- Fast, minimal UI
- Strict TypeScript types (no `any`)

## Testing

For development, use the "Reset Data" button in `/stats` to clear all data and test fresh flows.


