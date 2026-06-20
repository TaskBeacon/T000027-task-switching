# Task Plot Review

## Evidence Match

- Pass: title and construct match the Task Switching Task.
- Pass: rows reflect the controller-derived Start, Repeat, and Switch trial transition tags used for switch-cost analysis.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> Cue -> Decision -> Feedback -> ITI.
- Pass: timing labels match config: 300-600 ms fixation, 600 ms cue, 2000 ms decision, 800 ms feedback, 300-600 ms ITI.
- Pass: decision mapping shows F/J and preserves the parity and magnitude rule mappings.
- Pass: feedback shows correct, incorrect, or timeout with score update.
- Pass: no extra response keys, reward probabilities, or phases are shown.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
