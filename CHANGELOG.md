# CHANGELOG

All notable development changes for `T000027-task-switching` are documented here.

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
