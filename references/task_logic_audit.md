# Task Logic Audit: Task Switching Task

## 1. Paradigm Intent

- Task: `task_switching`.
- Construct: cognitive flexibility under cue-driven task-set reconfiguration.
- Manipulated trial factors:
- active rule (`parity` vs `magnitude`)
- transition type (`start`, `repeat`, `switch`)
- Primary dependent measures:
- decision accuracy (overall/switch/repeat)
- decision RT (overall/switch/repeat)
- switch cost (`RT_switch - RT_repeat`)
- timeout count and running score.

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `2` blocks x `48` trials.
- QA/sim profiles: `1` block x `24` trials.
- Block setup uses `Controller.start_block(block_idx)` to reset transition history.
- Trial specification uses `Controller.build_trial()` to sample rule/transition/digit.

### Trial State Machine

1. `fixation`
- Stimulus: `fixation`.
- Trigger: `fixation_onset`.
- Keys: none.

2. `cue`
- Stimuli: `cue_title`, `score_text`, rule cue (`cue_parity` or `cue_magnitude`), `trial_type_tag`.
- Trigger: `cue_onset`.
- Keys: none.

3. `decision`
- Stimuli: `score_text`, `target_digit`, `rule_prompt`, `key_hint`.
- Trigger: `decision_onset`.
- Response triggers: `choice_left` / `choice_right`.
- Timeout trigger: `choice_timeout`.

4. `feedback`
- Stimulus branch: `feedback_correct` or `feedback_incorrect` or `feedback_timeout`.
- Trigger branch: `feedback_correct` / `feedback_incorrect` / `feedback_timeout`.
- Keys: none.

5. `inter_trial_interval`
- Stimulus: `fixation`.
- Trigger: `iti_onset`.
- Keys: none.

## 3. Condition Semantics

- Runtime condition ID: `cued_switching`.
- Trial-level semantics are derived each trial:
- `task_rule`: `parity` or `magnitude`.
- `trial_type`: `start` on first trial, then `switch` or `repeat` relative to previous rule.
- `target_digit`: sampled from `[1,2,3,4,6,7,8,9]`.

## 4. Response and Scoring Rules

- Valid decision keys: `left_key` and `right_key` (default `f`/`j`).
- Rule-dependent correctness:
- parity rule: odd -> left, even -> right.
- magnitude rule: `<5` -> left, `>5` -> right.
- Timeout sets `is_correct = null` and applies `timeout_delta`.
- Score updates via controller:
- correct: `+1`
- incorrect: `-1`
- timeout: `0`

## 5. Stimulus Layout Plan

- Cue stage:
- `cue_title` at top (`0, 290`), `score_text` below (`0, 245`), rule cue center (`0, 95`), transition tag (`0, 20`).

- Decision stage:
- `score_text` top (`0, 245`), `target_digit` center (`0, 10`), `rule_prompt` lower (`0, -185`), `key_hint` (`0, -245`).

- Feedback stage:
- centered multiline text (`wrapWidth: 980`).

All participant-facing labels are sourced from config (`stimuli.*` and `task.rule_names` / `task.response_labels` / `task.trial_type_names`).

## 6. Trigger Plan

| Trigger | Code | Meaning |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation onset |
| `cue_onset` | 30 | cue onset |
| `decision_onset` | 40 | decision onset |
| `choice_left` | 41 | left response |
| `choice_right` | 42 | right response |
| `choice_timeout` | 43 | no response before deadline |
| `feedback_correct` | 50 | correct feedback onset |
| `feedback_incorrect` | 51 | incorrect feedback onset |
| `feedback_timeout` | 52 | timeout feedback onset |
| `iti_onset` | 60 | ITI onset |

## 7. Architecture Decisions (Auditability)

- `main.py` now follows the standardized single execution path for `human|qa|sim` with shared init order and mode-specific runtime context.
- `src/run_trial.py` implements task-switching-specific phases and removes MID leftovers (`anticipation`, `target`, `hit/miss` template flow).
- Decision response triggers are emitted explicitly (`choice_left`/`choice_right`) after response-key mapping, while timeout remains capture-policy driven.
- QA-required outputs (`condition`, `trial_id`, `task_rule`, `trial_type`, `target_digit`, `decision_response`, `decision_rt`, `is_correct`, `score_after`) are written each trial.

## 8. Inference Log

- Exact cue/fixation/ITI durations are inferred implementation parameters selected to satisfy phase separation and practical runtime constraints.
- `switch_probability = 0.5` is an inferred balancing choice to stabilize switch/repeat estimates, not a strict value mandated by any single source.
- Chinese localization strings were moved into config dictionaries to satisfy language-generic runtime contracts while preserving the same task logic.