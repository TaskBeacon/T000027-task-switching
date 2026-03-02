from __future__ import annotations

import random
from typing import Any

from psychopy import logging


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(round(float(value)))
    except Exception:
        return int(default)


def _as_int_list(value: Any, default: list[int]) -> list[int]:
    if not isinstance(value, (list, tuple)):
        return list(default)
    out: list[int] = []
    for item in value:
        try:
            out.append(int(item))
        except Exception:
            continue
    return out if out else list(default)


class Controller:
    """Task-level controller for cued task-switching trials."""

    def __init__(
        self,
        *,
        switch_probability: float = 0.5,
        digit_pool: list[int] | None = None,
        initial_score: int = 0,
        correct_delta: int = 1,
        incorrect_delta: int = -1,
        timeout_delta: int = 0,
        random_seed: int | None = None,
        enable_logging: bool = True,
    ) -> None:
        self.switch_probability = max(0.0, min(1.0, float(switch_probability)))
        self.digit_pool = list(digit_pool or [1, 2, 3, 4, 6, 7, 8, 9])
        self.initial_score = int(initial_score)
        self.correct_delta = int(correct_delta)
        self.incorrect_delta = int(incorrect_delta)
        self.timeout_delta = int(timeout_delta)
        self.enable_logging = bool(enable_logging)
        self.rng = random.Random(random_seed)

        self.current_score = int(initial_score)
        self.block_idx = -1
        self.trial_count_total = 0
        self.trial_count_block = 0
        self.previous_rule: str | None = None
        self.histories: list[dict[str, Any]] = []

    @classmethod
    def from_dict(cls, config: dict) -> "Controller":
        if not isinstance(config, dict):
            config = {}
        return cls(
            switch_probability=_safe_float(config.get("switch_probability", 0.5), 0.5),
            digit_pool=_as_int_list(config.get("digit_pool"), [1, 2, 3, 4, 6, 7, 8, 9]),
            initial_score=_safe_int(config.get("initial_score", 0), 0),
            correct_delta=_safe_int(config.get("correct_delta", 1), 1),
            incorrect_delta=_safe_int(config.get("incorrect_delta", -1), -1),
            timeout_delta=_safe_int(config.get("timeout_delta", 0), 0),
            random_seed=config.get("random_seed", None),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def start_block(self, block_idx: int) -> None:
        self.block_idx = int(block_idx)
        self.trial_count_block = 0
        self.previous_rule = None

    def next_trial_id(self) -> int:
        return int(self.trial_count_total) + 1

    def sample_duration(self, value: Any, default: float) -> float:
        if isinstance(value, (int, float)):
            return max(0.0, float(value))
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            low = _safe_float(value[0], default)
            high = _safe_float(value[1], default)
            if high < low:
                low, high = high, low
            return max(0.0, float(self.rng.uniform(low, high)))
        return max(0.0, float(default))

    def build_trial(self) -> dict[str, Any]:
        if self.previous_rule is None:
            task_rule = self.rng.choice(["parity", "magnitude"])
            trial_type = "start"
        else:
            do_switch = self.rng.random() < self.switch_probability
            if do_switch:
                task_rule = "magnitude" if self.previous_rule == "parity" else "parity"
            else:
                task_rule = self.previous_rule
            trial_type = "switch" if task_rule != self.previous_rule else "repeat"

        digit = int(self.rng.choice(self.digit_pool))
        self.previous_rule = task_rule
        return {
            "task_rule": task_rule,
            "trial_type": trial_type,
            "digit": digit,
            "switch_trial": trial_type == "switch",
        }

    def apply_score(self, is_correct: bool | None) -> dict[str, int]:
        score_before = int(self.current_score)
        if is_correct is None:
            delta = int(self.timeout_delta)
        elif is_correct:
            delta = int(self.correct_delta)
        else:
            delta = int(self.incorrect_delta)
        score_after = int(score_before + delta)
        self.current_score = score_after
        return {
            "score_before": score_before,
            "score_after": score_after,
            "score_delta": int(delta),
        }

    def record_trial(self, record: dict[str, Any]) -> None:
        self.trial_count_total += 1
        self.trial_count_block += 1
        self.histories.append(dict(record))

        if self.enable_logging:
            logging.data(
                "[TaskSwitching] "
                f"block={self.block_idx} "
                f"trial_block={self.trial_count_block} "
                f"trial_total={self.trial_count_total} "
                f"rule={record.get('task_rule', '')} "
                f"trial_type={record.get('trial_type', '')} "
                f"digit={record.get('target_digit', '')} "
                f"resp={record.get('response_key', '')} "
                f"correct={record.get('is_correct', None)} "
                f"score={record.get('score_after', self.current_score)}"
            )
