from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for cue-based task-switching decision trials."""

    quality_rate_repeat: float = 0.86
    quality_rate_switch: float = 0.74
    miss_rate: float = 0.06
    rt_repeat_mean_s: float = 0.58
    rt_switch_mean_s: float = 0.72
    rt_sd_s: float = 0.12
    rt_min_s: float = 0.20

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.quality_rate_repeat = max(0.0, min(1.0, float(self.quality_rate_repeat)))
        self.quality_rate_switch = max(0.0, min(1.0, float(self.quality_rate_switch)))
        self.miss_rate = max(0.0, min(1.0, float(self.miss_rate)))
        self.rt_repeat_mean_s = float(self.rt_repeat_mean_s)
        self.rt_switch_mean_s = float(self.rt_switch_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _continue_action(self, valid_keys: list[str], phase: str) -> Action:
        key = "space" if "space" in valid_keys else valid_keys[0]
        rt = max(self.rt_min_s, self._sample_normal(self.rt_repeat_mean_s, self.rt_sd_s))
        return Action(
            key=key,
            rt_s=rt,
            meta={"source": "task_sampler", "phase": phase, "outcome": "continue"},
        )

    def act(self, obs: Observation) -> Action:
        valid_keys = [str(k).strip().lower() for k in list(obs.valid_keys or []) if str(k).strip()]
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        if self._rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        phase = str(obs.phase or "")
        if phase != "decision":
            return self._continue_action(valid_keys, phase)

        if self._sample_random() < self.miss_rate:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "outcome": "timeout"})

        factors = dict(obs.task_factors or {})
        left_key = str(factors.get("left_key", "f")).strip().lower()
        right_key = str(factors.get("right_key", "j")).strip().lower()
        correct_key = str(factors.get("correct_key", "")).strip().lower()
        trial_type = str(factors.get("trial_type", "")).strip().lower()

        if left_key not in valid_keys:
            left_key = valid_keys[0]
        if right_key not in valid_keys:
            right_key = valid_keys[-1] if len(valid_keys) > 1 else valid_keys[0]

        if correct_key not in valid_keys:
            correct_key = left_key

        incorrect_key = right_key if correct_key == left_key else left_key

        if trial_type == "switch":
            quality_rate = self.quality_rate_switch
            rt_mean = self.rt_switch_mean_s
        else:
            quality_rate = self.quality_rate_repeat
            rt_mean = self.rt_repeat_mean_s

        choose_correct = self._sample_random() < quality_rate
        chosen_key = correct_key if choose_correct else incorrect_key
        rt = max(self.rt_min_s, self._sample_normal(rt_mean, self.rt_sd_s))

        return Action(
            key=chosen_key,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "outcome": "choose",
                "trial_type": trial_type,
                "quality_rate": quality_rate,
            },
        )
