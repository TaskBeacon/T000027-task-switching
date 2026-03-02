# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['cued_switching']` | W2023626050 | Mixed-task switching is implemented as within-stream cue transitions (`switch` vs `repeat`). | inferred | Condition label is stable while transition type varies trial-by-trial. |
| task.keys | `task.key_list`, `task.left_key`, `task.right_key` | `['f','j','space']`, left=`f`, right=`j` | W1969112442 | Binary categorical response under an active rule is standard in cued task-switching paradigms. | inferred | `space` remains reserved for continue screens. |
| task.localization.rule_names | `task.rule_names` | parity=`奇偶判断`, magnitude=`大小判断` | W2023626050 | Rule cue identity must be explicit for participant task-set preparation. | inferred | Moved to config for localization-ready runtime behavior. |
| task.localization.response_labels | `task.response_labels` | parity: `奇数/偶数`; magnitude: `小于5/大于5` | W1969112442 | Rule-dependent category mapping is required to define correct response under each task-set. | inferred | No participant-facing label is hardcoded in runtime code. |
| timing.fixation | `timing.fixation_duration` | `[0.3, 0.6]` s jitter | W2154099072 | Event separation with pre-cue fixation supports clearer epoch boundaries. | inferred | Sampled per trial by controller. |
| timing.cue | `timing.cue_duration` | `0.6` s | W2023626050 | Distinct cue period supports task-set reconfiguration before target response. | inferred | Fixed in this implementation profile. |
| timing.decision_deadline | `timing.decision_deadline` | `2.0` s | W1969112442 | Bounded response windows enable omission-sensitive accuracy metrics. | inferred | Timeout emits dedicated trigger and feedback. |
| timing.feedback | `timing.feedback_duration` | `0.8` s | W2080507226 | Explicit post-response feedback is compatible with performance-monitoring variants. | inferred | Correct/incorrect/timeout feedback are separately coded. |
| timing.iti | `timing.iti_duration` | `[0.3, 0.6]` s jitter | W2023626050 | Inter-trial jitter reduces temporal expectancy and carry-over effects. | inferred | Sampled per trial by controller. |
| controller.switch_probability | `controller.switch_probability` | `0.5` | W2023626050 | Switch/repeat balance supports stable switch-cost estimation. | inferred | First trial is tagged `start`; later trials become `switch` or `repeat`. |
| controller.digit_pool | `controller.digit_pool` | `[1,2,3,4,6,7,8,9]` | W2312817634 | Excluding `5` avoids ambiguity for magnitude decisions. | inferred | Supports parity and magnitude task-sets with same stimuli. |
| controller.scoring | `controller.correct_delta`, `controller.incorrect_delta`, `controller.timeout_delta` | `+1`, `-1`, `0` | W2080507226 | Trial-level outcome coding supports online performance monitoring. | inferred | Score is reported in cue/feedback and summaries. |
| trigger.cue_and_decision | `triggers.map.cue_onset`, `triggers.map.decision_onset` | `30`, `40` | W2154099072 | Cue and decision stages should be separable for timing/audit analyses. | inferred | `fixation_onset` and `iti_onset` bound each trial. |
| trigger.response | `triggers.map.choice_left`, `triggers.map.choice_right`, `triggers.map.choice_timeout` | `41`, `42`, `43` | W1969112442 | Response identity and omissions are primary behavioral events in switching tasks. | inferred | Left/right response triggers are emitted after captured key mapping. |
| trigger.feedback | `triggers.map.feedback_correct`, `triggers.map.feedback_incorrect`, `triggers.map.feedback_timeout` | `50`, `51`, `52` | W2080507226 | Outcome-separated feedback markers support error/monitoring analysis. | inferred | Feedback onset code matches outcome branch in runtime. |