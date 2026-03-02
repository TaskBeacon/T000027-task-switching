# CHANGELOG

All notable development changes for `T000027-task-switching` are documented here.

## [v0.2.1-dev] - 2026-03-02

### Changed
- Standardized `main.py` to the single-flow `human|qa|sim` runtime contract with shared initialization and runtime-context handling.
- Replaced `src/run_trial.py` MID-template leftovers with task-switching-specific phases (`fixation -> cue -> decision -> feedback -> inter_trial_interval`) using controller-built rule transitions.
- Added config-driven localization dictionaries in all config profiles (`task.rule_names`, `task.trial_type_names`, `task.response_labels`) and introduced `stimuli.target_digit` for dynamic target rendering.
- Rewrote references artifacts to current contracts:
  - `references/references.yaml`
  - `references/references.md`
  - `references/parameter_mapping.md`
  - `references/stimulus_mapping.md`
  - `references/task_logic_audit.md`

### Fixed
- Fixed YAML parsing failure in `references/references.yaml` caused by unquoted colon-containing titles.
- Restored required reference artifact headings/columns expected by validators.
- Restored QA-required trial output fields (`condition`, `trial_id`, `task_rule`, `trial_type`, `target_digit`, `decision_response`, `decision_rt`, `is_correct`, `score_after`).

### Validation
- `python -m py_compile main.py src/run_trial.py`
- `python e:/Taskbeacon/psyflow/scripts/check_task_standard.py --task-path e:/Taskbeacon/T000027-task-switching`
- `psyflow-qa e:/Taskbeacon/T000027-task-switching --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
- `python -m psyflow.validate e:/Taskbeacon/T000027-task-switching`

## [v0.2.0-dev] - 2026-02-19

### Changed
- Rebuilt the task from zero-base literature logic into a cue-based task-switching paradigm (`fixation -> cue -> decision -> feedback -> iti`).
- Replaced MID-template runtime code in `main.py`, `src/run_trial.py`, and `src/utils.py` with rule-transition and switch-cost-capable logic.
- Rewrote all `config/*.yaml` files with clean UTF-8 Chinese participant stimuli and task-switching-specific trigger/response mapping.
- Replaced sampler responder with task-switching decision policy in `responders/task_sampler.py`.
- Replaced poisoned literature artifacts with curated task-switching evidence in `references/references.yaml`, `references/references.md`, `references/selected_papers.json`, `references/task_logic_audit.md`, `references/stimulus_mapping.md`, and `references/parameter_mapping.md`.
- Updated metadata/docs (`README.md`, `taskbeacon.yaml`).

### Fixed
- Removed MID-style hit/miss/duration adaptation assumptions that were invalid for task-switching paradigms.
- Removed corrupted participant-facing text encoding artifacts across config files.

## [v0.1.1-dev] - 2026-02-19

### Changed
- Rebuilt literature bundle with task-relevant curated papers and regenerated reference artifacts.
- Replaced corrupted `references/task_logic_audit.md` with a full state-machine audit.
- Updated `references/stimulus_mapping.md` to concrete implemented stimulus IDs per condition.
- Synced metadata (`README.md`, `taskbeacon.yaml`) with current configuration and evidence.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Task Switching Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
