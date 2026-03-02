# Stimulus Mapping

Task: `Task Switching Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `cued_switching` | `cue_parity`, `cue_magnitude`, `trial_type_tag`, `rule_prompt`, `key_hint`, runtime digit target (`target_digit`), `feedback_correct`, `feedback_incorrect`, `feedback_timeout`, `fixation` | `W2023626050` | Cued task-switching paradigms separate cue-based preparation and stimulus-driven response stages with measurable switch/repeat costs. | `psychopy_builtin` | Rule cue and digit target are concretely rendered each trial; switch/repeat labels are derived from rule transition. |
| `response_selection_logic` | dynamic key mapping text and correctness-specific feedback panels | `W1969112442` | Cue-based preparation and stimulus-based processing jointly shape task-switching performance and response mapping effects. | `psychopy_builtin` | Mapping text updates per active rule to prevent ambiguity under rapid switching. |
| `all_conditions` | `instruction_text`, `score_text`, `block_break`, `good_bye` | `W2080507226` | Task-switching studies report accuracy/RT and switching cost summaries that require explicit task envelope screens. | `psychopy_builtin` | Summary screens expose block/session metrics including switch cost. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config or runtime drawing.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
