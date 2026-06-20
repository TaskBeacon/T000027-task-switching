Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Task Switching Task
Construct: cognitive flexibility / task switching / switch cost
Rows/conditions:
- Start: first trial or no previous rule.
- Repeat: current rule repeats the previous rule.
- Switch: current rule differs from the previous rule.

Timeline phases:
- Start: Fixation (300-600 ms; no response; +) -> Cue (600 ms; no response; parity or magnitude rule; Start tag) -> Decision (2000 ms; press F/J; digit 1,2,3,4,6,7,8,9) -> Feedback (800 ms; no response; correct / incorrect / timeout; score update) -> ITI (300-600 ms; no response; +)
- Repeat: Fixation (300-600 ms; no response; +) -> Cue (600 ms; no response; same rule as previous; Repeat tag) -> Decision (2000 ms; press F/J; digit 1,2,3,4,6,7,8,9) -> Feedback (800 ms; no response; correct / incorrect / timeout; score update) -> ITI (300-600 ms; no response; +)
- Switch: Fixation (300-600 ms; no response; +) -> Cue (600 ms; no response; rule changes; Switch tag) -> Decision (2000 ms; press F/J; digit 1,2,3,4,6,7,8,9) -> Feedback (800 ms; no response; correct / incorrect / timeout; score update) -> ITI (300-600 ms; no response; +)

Decision rule mapping:
- Parity rule: F=odd, J=even.
- Magnitude rule: F=less than 5, J=greater than 5.

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per transition type.
- Each row contains 5 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows participant-visible screen content only.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place transition labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 18-20% of the image.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- Preserve these exact terms where used: Start, Repeat, Switch, parity, magnitude, F=odd, J=even, F=less than 5, J=greater than 5, 300-600 ms, 600 ms, 2000 ms, 800 ms.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
