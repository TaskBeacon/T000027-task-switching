# Task Switching Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Task Switching Task |
| Version | v0.1.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000027-task-switching |
| Short Description | Cognitive flexibility paradigm with repeat/switch/mixed conditions. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-18 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | English |
| Voice Name |  |

## 1. Task Overview

This task implements a task-switching paradigm with condition labels `repeat`, `switch`, and `mixed`. Trials include cue presentation, an anticipation phase, target response capture, and feedback.

The implementation logs condition-wise response performance and supports human, QA, scripted simulation, and sampler simulation execution profiles through dedicated config files.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Prepare block | A block condition schedule is loaded into `BlockUnit`. |
| 2. Run trials | `run_trial(...)` executes cue, anticipation, target, and feedback phases. |
| 3. Show block summary | Block accuracy and score are shown. |
| 4. End task | Final score summary is shown at experiment completion. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Cue | Condition-specific cue (`repeat`, `switch`, `mixed`) is shown. |
| Anticipation | Fixation phase with response monitoring. |
| Target | Condition-specific target appears with key capture. |
| Pre-feedback fixation | Brief fixation interval before feedback. |
| Feedback | Hit/miss feedback and score delta are shown. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive target duration | Controller adjusts target duration toward target accuracy. |
| Condition tracking | Per-condition histories are updated after each trial. |
| Accuracy-linked scoring | Feedback state reflects trial hit/miss outcome. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `anticipation` | Pre-target response-monitoring period. |
| `target` | Main response window for target stimulus. |

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
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `repeat_cue`, `switch_cue`, `mixed_cue` | text | Condition cue prompts. |
| `repeat_target`, `switch_target`, `mixed_target` | text | Condition targets for response capture. |
| `*_hit_feedback`, `*_miss_feedback` | text | Condition-specific feedback text. |
| `fixation`, `block_break`, `good_bye` | text | Shared fixation and summary screens. |

### d. Timing

| Phase | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 1.0 s |
| prefeedback | 0.4 s |
| feedback | 0.8 s |
| target | adaptive via controller (`0.08`-`0.40` s bounds) |

## 4. Methods (for academic publication)

Participants completed a task-switching protocol with repeat, switch, and mixed condition trials. Each trial contained condition cueing, a brief anticipation period, a response window for the target, and immediate feedback.

The procedure supports estimation of condition-wise performance under switching demands using accuracy and response timing logs. The adaptive controller maintains target difficulty by adjusting response-window duration according to recent trial outcomes.

The task emits explicit trigger events for cue, anticipation, target, response, and feedback stages to support synchronized acquisition contexts.
