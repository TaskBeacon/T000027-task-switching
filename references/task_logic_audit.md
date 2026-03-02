# Task Logic Audit: Task Switching Task

## 1. Paradigm Intent

- Task: `task_switching`
- Primary construct: cognitive flexibility in cued rule switching.
- Manipulated factors:
  - task rule (`parity` vs `magnitude`)
  - transition type (`switch` vs `repeat`), defined relative to prior trial rule
- Dependent measures:
  - decision accuracy (overall / switch / repeat)
  - decision reaction time (overall / switch / repeat)
  - switch cost (`RT_switch - RT_repeat`)
  - timeout count
  - cumulative score trajectory
- Key citations:
  - `W2154099072`
  - `W2080507226`
  - `W2023626050`
  - `W1969112442`
  - `W2312817634`

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: `2` (human baseline), `1` (QA/sim profiles).
- Trials per block: `48` (human baseline), `24` (QA/sim profiles).
- Randomization/counterbalancing:
  - trial rule sampled online from controller using `switch_probability`
  - `switch/repeat` is derived from rule transition against previous trial
  - digit target sampled from pool `[1,2,3,4,6,7,8,9]`

### Trial State Machine

1. `fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: central fixation (`+`)
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after jittered fixation duration
   - Next state: `cue`

2. `cue`
   - Onset trigger: `cue_onset`
   - Stimuli shown together:
     - cue title
     - current score
     - rule cue (`奇偶判断` or `大小判断`)
     - trial-type tag (`起始/重复/切换`)
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after fixed cue duration
   - Next state: `decision`

3. `decision`
   - Onset trigger: `decision_onset`
   - Stimuli shown together:
     - current score text
     - rule prompt
     - key mapping hint for current rule
     - single target digit
   - Valid keys: `[left_key, right_key]` (default `F/J`)
   - Response triggers:
     - `choice_left`
     - `choice_right`
   - Timeout trigger: `choice_timeout`
   - Timeout behavior: no decision response recorded; proceed to timeout feedback
   - Next state: `feedback`

4. `feedback`
   - Onset trigger (outcome-dependent):
     - `feedback_correct`
     - `feedback_incorrect`
     - `feedback_timeout`
   - Stimuli shown:
     - correctness feedback with predicted/true category and score update, or
     - timeout feedback with true category and score
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after feedback duration
   - Next state: `iti`

5. `iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: fixation (`+`)
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after jittered ITI
   - Next state: next trial

## 3. Condition Semantics

- Condition ID: `cued_switching`
  - Participant-facing meaning: each trial uses an explicit rule cue, then participant categorizes one digit under that rule.
  - Concrete stimulus realization:
    - rule cue text (`规则：奇偶判断` / `规则：大小判断`)
    - single large digit target in center
    - dynamic key hint tied to current rule
  - Outcome rules:
    - parity rule: odd vs even
    - magnitude rule: less-than-5 vs greater-than-5
    - correctness based on rule-consistent category mapping
    - switch/repeat tag computed from current vs previous rule

## 4. Response and Scoring Rules

- Response mapping (default):
  - left key (`F`) selects left category label
  - right key (`J`) selects right category label
- Rule-specific category mapping:
  - parity: `F=奇数`, `J=偶数`
  - magnitude: `F=小于5`, `J=大于5`
- Missing-response policy:
  - timeout emits `choice_timeout`
  - timeout trial uses `timeout_delta` (configured as `0`)
- Correctness logic:
  - `is_correct = (response_key == correct_key)` when responded
- Score updates:
  - correct: `+1`
  - incorrect: `-1`
  - timeout: `0`
- Running metrics:
  - accuracy by transition type
  - RT by transition type
  - switch cost in milliseconds
  - timeout count and cumulative score

## 5. Stimulus Layout Plan

- Cue screen (`cue`):
  - `cue_title` at top center (`0, 290`)
  - `score_text` below title (`0, 245`)
  - rule cue text centered (`0, 95`)
  - trial-type tag below cue (`0, 20`)

- Decision screen (`decision`):
  - `score_text` top area (`0, 245`)
  - `rule_prompt` lower center (`0, -185`)
  - `key_hint` below rule prompt (`0, -245`)
  - target digit centered (`0, 10`), large font for salience

- Feedback screen (`feedback`):
  - centered multiline outcome text (`wrapWidth <= 980`)

All participant-facing text is Chinese and uses `font: SimHei`.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation onset |
| `cue_onset` | 30 | rule cue onset |
| `decision_onset` | 40 | decision screen onset |
| `choice_left` | 41 | left-key response |
| `choice_right` | 42 | right-key response |
| `choice_timeout` | 43 | no response before deadline |
| `feedback_correct` | 50 | correct feedback onset |
| `feedback_incorrect` | 51 | incorrect feedback onset |
| `feedback_timeout` | 52 | timeout feedback onset |
| `iti_onset` | 60 | ITI onset |

## 7. Inference Log

- Decision: represent task switching as one runtime condition (`cued_switching`) with trial-level transition coding (`switch/repeat`).
- Why inference was required: task-switching literature manipulates within-task rule transitions rather than independent block condition labels.
- Citation-supported rationale: selected task-switching papers quantify performance using transition-type costs, consistent with this implementation.

- Decision: use explicit Chinese textual cues for rule identity and dynamic key-hint overlays each trial.
- Why inference was required: publications vary between symbolic and textual cue designs.
- Citation-supported rationale: preserves core cue-based preparation and response-selection mechanisms while keeping participant instructions unambiguous.
