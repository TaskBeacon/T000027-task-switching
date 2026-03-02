# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['cued_switching']` | `W2023626050` | `supported` | Cued task-switching is implemented as one paradigm stream with within-stream switch/repeat transitions. |
| `task.key_list` | `['f', 'j', 'space']` | `W1969112442` | `inferred` | Binary decision mapping aligns with two-category responses under each active rule. |
| `task.total_blocks` | `2` | `W2080507226` | `inferred` | Multi-block design enables stable switch/repeat estimates while preserving manageable run length. |
| `task.trial_per_block` | `48` | `W2023626050` | `inferred` | Sufficient trial count for reliable switch-cost estimation in behavioral runs. |
| `timing.fixation_duration` | `[0.3, 0.6]` | `W2154099072` | `inferred` | Jittered fixation reduces temporal expectancy and separates trial events. |
| `timing.cue_duration` | `0.6` | `W2023626050` | `inferred` | Distinct cue interval supports rule preparation before target processing. |
| `timing.decision_deadline` | `2.0` | `W1969112442` | `inferred` | Bounded response window yields timeout-sensitive cognitive control metrics. |
| `timing.feedback_duration` | `0.8` | `W2080507226` | `inferred` | Brief explicit correctness feedback supports performance monitoring. |
| `controller.switch_probability` | `0.5` | `W2023626050` | `inferred` | Balanced switch/repeat sampling approximates canonical mixed-task-switching sequences. |
| `controller.digit_pool` | `[1,2,3,4,6,7,8,9]` | `W2312817634` | `inferred` | Excludes ambiguous midpoint value and supports parity/magnitude dual-rule mapping. |
| `controller.correct_delta` | `+1` | `W2080507226` | `inferred` | Signed score updates provide transparent trial-level performance feedback. |
| `controller.incorrect_delta` | `-1` | `W2080507226` | `inferred` | Symmetric penalty keeps cumulative score sensitive to switch-related errors. |
| `controller.timeout_delta` | `0` | `W2080507226` | `inferred` | Timeout is behaviorally logged without reward bias. |
| `triggers.map.cue_onset` | `30` | `W2154099072` | `inferred` | Explicit cue-stage marker for cue-based preparation analysis. |
| `triggers.map.decision_onset` | `40` | `W2154099072` | `inferred` | Isolates decision epoch from preparatory cue epoch. |
| `triggers.map.choice_left` | `41` | `W1969112442` | `inferred` | Captures response identity under dynamic rule mapping. |
| `triggers.map.choice_right` | `42` | `W1969112442` | `inferred` | Captures response identity under dynamic rule mapping. |
| `triggers.map.feedback_correct` | `50` | `W2080507226` | `inferred` | Outcome-specific feedback marker for monitoring effects. |
| `triggers.map.feedback_incorrect` | `51` | `W2080507226` | `inferred` | Outcome-specific feedback marker for monitoring effects. |
| `triggers.map.feedback_timeout` | `52` | `W2080507226` | `inferred` | Timeout feedback marker for omission analysis. |
