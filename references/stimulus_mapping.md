# Stimulus Mapping

Task: `Task Switching Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `repeat` | `repeat_cue`, `repeat_target` | `W2100359507` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for REPEAT; target token for condition-specific response context. |
| `switch` | `switch_cue`, `switch_target` | `W2100359507` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for SWITCH; target token for condition-specific response context. |
| `mixed` | `mixed_cue`, `mixed_target` | `W2100359507` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for MIXED; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
