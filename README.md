# Task Switching Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Task Switching Task |
| Version | v0.2.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000027-task-switching |
| Short Description | Cued task-switching paradigm with explicit rule transitions and switch-cost metrics. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements a cue-based task-switching paradigm. Each trial first presents a rule cue (`奇偶判断` or `大小判断`), then a target digit appears and participants respond with a two-key mapping.

The implementation computes trial transitions (`switch/repeat`) online and records accuracy, reaction time, timeout behavior, and cumulative score, enabling direct switch-cost analysis.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Block init | Controller resets block counters and transition history. |
| 2. Trial loop | `run_trial(...)` executes fixation, cue, decision, feedback, and ITI for each trial. |
| 3. Block summary | Display accuracy, switch/repeat accuracy, mean RT, switch cost, and score. |
| 4. Final summary | Display session-level switching metrics and final score. |

### Trial-Level Flow

| Step | Description |
|---|---|
| `fixation` | Jittered fixation baseline before cue. |
| `cue` | Show active rule and trial transition tag (`起始/重复/切换`). |
| `decision` | Present one digit and capture `F/J` response under current rule. |
| `feedback` | Show correct/incorrect/timeout feedback with score update. |
| `iti` | Jittered inter-trial fixation. |

### Controller Logic

| Component | Description |
|---|---|
| Rule transition sampling | Controller samples current rule based on `switch_probability`, then derives `trial_type`. |
| Target generation | Digit target sampled from `[1,2,3,4,6,7,8,9]`. |
| Scoring | Correct `+1`, incorrect `-1`, timeout `0`. |
| Metrics | Supports accuracy/RT for overall, switch, repeat, and switch-cost derivation. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `fixation` | Pre-trial baseline. |
| `cue` | Rule cue preparation stage. |
| `decision` | Active response window for digit categorization. |
| `feedback` | Outcome feedback stage. |
| `iti` | Inter-trial transition stage. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `black` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Stimulus Group | Description |
|---|---|
| `cue_parity`, `cue_magnitude`, `trial_type_tag` | Rule cue and transition label stimuli. |
| Runtime `target_digit` | Single large digit target rendered during decision phase. |
| `rule_prompt`, `key_hint` | Rule-specific response mapping prompts. |
| `feedback_correct`, `feedback_incorrect`, `feedback_timeout` | Outcome-dependent feedback texts. |
| `instruction_text`, `score_text`, `block_break`, `good_bye`, `fixation` | Envelope and summary stimuli. |

### d. Timing

| Stage | Duration |
|---|---|
| fixation | jittered (`[0.3, 0.6] s`) |
| cue | fixed (`0.6 s`) |
| decision | deadline (`2.0 s`) |
| feedback | fixed (`0.8 s`) |
| iti | jittered (`[0.3, 0.6] s`) |

### e. Triggers

| Trigger | Code |
|---|---:|
| `exp_onset` | 1 |
| `exp_end` | 2 |
| `block_onset` | 10 |
| `block_end` | 11 |
| `fixation_onset` | 20 |
| `cue_onset` | 30 |
| `decision_onset` | 40 |
| `choice_left` | 41 |
| `choice_right` | 42 |
| `choice_timeout` | 43 |
| `feedback_correct` | 50 |
| `feedback_incorrect` | 51 |
| `feedback_timeout` | 52 |
| `iti_onset` | 60 |

### f. Adaptive Controller

| Parameter Group | Description |
|---|---|
| `switch_probability` | Controls likelihood of rule switch vs repeat on each trial. |
| `digit_pool` | Candidate target digits used for categorization. |
| `score_deltas` | Signed score update policy for correct/incorrect/timeout trials. |
| `random_seed` | Enables deterministic QA/sim behavior when set. |

## 4. Methods (for academic publication)

Participants completed a cued task-switching paradigm in which each trial provided an explicit rule cue followed by a single digit requiring binary categorization. Rule transitions were sampled online to create repeat and switch trials, enabling estimation of switching-specific performance costs.

Trial-level outputs include task rule, transition type, target digit, response, correctness, reaction time, timeout status, and cumulative score. The implementation emits trigger-aligned phase events (`fixation`, `cue`, `decision`, `feedback`, `iti`) for reproducible behavioral and synchronized acquisition workflows.
