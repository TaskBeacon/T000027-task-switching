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


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def as_dict(value: Any) -> dict:
    return value if isinstance(value, dict) else {}


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(sum(values) / len(values))


def _accuracy(rows: list[dict]) -> float:
    values = [row.get("is_correct", None) for row in rows if row.get("is_correct", None) is not None]
    if not values:
        return 0.0
    return float(sum(1 for value in values if _as_bool(value)) / len(values))


def _decision_rt_s(row: dict) -> float | None:
    try:
        return float(row.get("decision_rt_s", row.get("decision_rt", None)))
    except Exception:
        return None


def normalize_generated_condition_rows(rows: list[dict[str, Any]]) -> None:
    """Keep public condition scalar after BlockUnit stores generated specs."""
    for row in rows:
        condition = row.get("condition")
        if isinstance(condition, dict):
            row["condition"] = str(condition.get("condition", "cued_switching"))
        elif isinstance(condition, (list, tuple)) and condition:
            row["condition"] = str(condition[0])


def parse_task_switching_condition(condition: Any) -> dict[str, Any]:
    """Decode a scheduled task-switching condition."""
    if isinstance(condition, (list, tuple)) and len(condition) >= 9:
        (
            condition_name,
            condition_id,
            trial_index,
            task_rule,
            trial_type,
            target_digit,
            switch_trial,
            fixation_duration,
            iti_duration,
            *_,
        ) = condition
        return {
            "condition": str(condition_name).strip().lower(),
            "condition_id": str(condition_id),
            "trial_index": int(trial_index),
            "task_rule": str(task_rule).strip().lower(),
            "trial_type": str(trial_type).strip().lower(),
            "target_digit": int(target_digit),
            "switch_trial": bool(switch_trial),
            "fixation_duration": fixation_duration,
            "iti_duration": iti_duration,
        }
    if isinstance(condition, dict):
        condition_name = str(condition.get("condition", "cued_switching")).strip().lower()
        return {
            "condition": condition_name,
            "condition_id": str(condition.get("condition_id", condition_name)),
            "trial_index": int(condition.get("trial_index", 1)),
            "task_rule": str(condition.get("task_rule", "parity")).strip().lower(),
            "trial_type": str(condition.get("trial_type", "repeat")).strip().lower(),
            "target_digit": int(condition.get("target_digit", condition.get("digit", 1))),
            "switch_trial": bool(condition.get("switch_trial", False)),
            "fixation_duration": condition.get("fixation_duration", None),
            "iti_duration": condition.get("iti_duration", None),
        }
    return {
        "condition": str(condition).strip().lower(),
        "condition_id": str(condition).strip().lower(),
        "trial_index": 1,
        "task_rule": "parity",
        "trial_type": "start",
        "target_digit": 1,
        "switch_trial": False,
        "fixation_duration": None,
        "iti_duration": None,
    }


def task_switching_rule_profile(task_rule: str, target_digit: int, left_key: str, right_key: str, settings) -> dict[str, Any]:
    """Resolve task rule labels, correct response, and scoring category."""
    rule_names = as_dict(getattr(settings, "rule_names", {}))
    response_labels = as_dict(getattr(settings, "response_labels", {}))

    rule_key = "magnitude" if task_rule == "magnitude" else "parity"
    localized_rule_name = str(rule_names.get(rule_key, rule_key))

    rule_labels = as_dict(response_labels.get(rule_key, {}))
    if rule_key == "parity":
        left_label = str(rule_labels.get("left", "odd"))
        right_label = str(rule_labels.get("right", "even"))
        is_left_correct = bool(target_digit % 2 == 1)
        correct_category = "odd" if is_left_correct else "even"
    else:
        left_label = str(rule_labels.get("left", "<5"))
        right_label = str(rule_labels.get("right", ">5"))
        is_left_correct = bool(target_digit < 5)
        correct_category = "lt5" if is_left_correct else "gt5"

    correct_key = left_key if is_left_correct else right_key
    correct_label = left_label if is_left_correct else right_label

    return {
        "rule": rule_key,
        "rule_name": localized_rule_name,
        "left_label": left_label,
        "right_label": right_label,
        "correct_key": correct_key,
        "correct_category": correct_category,
        "correct_label": correct_label,
    }


def summarize_trials(trials: list[dict], fallback_score: int = 0) -> dict[str, float | int]:
    if not trials:
        return {
            "accuracy": 0.0,
            "switch_accuracy": 0.0,
            "repeat_accuracy": 0.0,
            "timeout_count": 0,
            "mean_rt_ms": 0.0,
            "mean_switch_rt_ms": 0.0,
            "mean_repeat_rt_ms": 0.0,
            "switch_cost_ms": 0.0,
            "score_end": int(fallback_score),
            "net_score": 0,
        }

    timeout_count = sum(1 for row in trials if _as_bool(row.get("decision_timed_out", False)))
    responded = [row for row in trials if not _as_bool(row.get("decision_timed_out", False))]
    switch_rows = [row for row in responded if str(row.get("trial_type", "")).strip().lower() == "switch"]
    repeat_rows = [row for row in responded if str(row.get("trial_type", "")).strip().lower() == "repeat"]

    rt_values = [_decision_rt_s(row) for row in responded]
    rt_values = [value for value in rt_values if value is not None]
    mean_rt_ms = _mean(rt_values) * 1000.0 if rt_values else 0.0

    switch_rt_values = [_decision_rt_s(row) for row in switch_rows]
    switch_rt_values = [value for value in switch_rt_values if value is not None]
    mean_switch_rt_ms = _mean(switch_rt_values) * 1000.0 if switch_rt_values else 0.0

    repeat_rt_values = [_decision_rt_s(row) for row in repeat_rows]
    repeat_rt_values = [value for value in repeat_rt_values if value is not None]
    mean_repeat_rt_ms = _mean(repeat_rt_values) * 1000.0 if repeat_rt_values else 0.0

    switch_cost_ms = mean_switch_rt_ms - mean_repeat_rt_ms if switch_rt_values and repeat_rt_values else 0.0

    score_end = int(fallback_score)
    for row in reversed(trials):
        if row.get("score_after", None) is not None:
            score_end = _safe_int(row.get("score_after"), fallback_score)
            break

    net_score = sum(_safe_int(row.get("score_delta", 0), 0) for row in trials)
    return {
        "accuracy": _accuracy(responded),
        "switch_accuracy": _accuracy(switch_rows),
        "repeat_accuracy": _accuracy(repeat_rows),
        "timeout_count": int(timeout_count),
        "mean_rt_ms": float(mean_rt_ms),
        "mean_switch_rt_ms": float(mean_switch_rt_ms),
        "mean_repeat_rt_ms": float(mean_repeat_rt_ms),
        "switch_cost_ms": float(switch_cost_ms),
        "score_end": int(score_end),
        "net_score": int(net_score),
    }


class Controller:
    """Task-level controller for cued task-switching trials."""

    def __init__(
        self,
        *,
        initial_score: int = 0,
        correct_delta: int = 1,
        incorrect_delta: int = -1,
        timeout_delta: int = 0,
        enable_logging: bool = True,
    ) -> None:
        self.initial_score = int(initial_score)
        self.correct_delta = int(correct_delta)
        self.incorrect_delta = int(incorrect_delta)
        self.timeout_delta = int(timeout_delta)
        self.enable_logging = bool(enable_logging)

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
            initial_score=_safe_int(config.get("initial_score", 0), 0),
            correct_delta=_safe_int(config.get("correct_delta", 1), 1),
            incorrect_delta=_safe_int(config.get("incorrect_delta", -1), -1),
            timeout_delta=_safe_int(config.get("timeout_delta", 0), 0),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def start_block(self, block_idx: int) -> None:
        self.block_idx = int(block_idx)
        self.trial_count_block = 0
        self.previous_rule = None

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


def _sample_duration(rng: random.Random, value: Any, default: float) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, float(value))
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        low = _safe_float(value[0], default)
        high = _safe_float(value[1], default)
        if high < low:
            low, high = high, low
        return max(0.0, float(rng.uniform(low, high)))
    return max(0.0, float(default))


def generate_task_switching_conditions(
    n_trials: int,
    condition_labels: list[Any] | None,
    *,
    seed: int,
    switch_probability: float = 0.5,
    digit_pool: list[int] | None = None,
    fixation_duration: Any = 0.45,
    iti_duration: Any = 0.45,
    random_seed: int | None = None,
    seed_offset: int = 0,
    enable_logging: bool = True,
    **kwargs,
) -> list[tuple[Any, ...]]:
    """Generate auditable task-switching trial specs for BlockUnit."""
    del kwargs

    labels = [str(label) for label in (condition_labels or ["cued_switching"])]
    condition_name = labels[0] if labels else "cued_switching"
    n = int(n_trials)
    if n <= 0:
        return []

    base_seed = int(seed if random_seed is None else random_seed) + int(seed_offset)
    trial_rng = random.Random(base_seed)
    timing_rng = random.Random(base_seed + 10_000_019)
    switch_p = max(0.0, min(1.0, float(switch_probability)))
    digits = _as_int_list(digit_pool, [1, 2, 3, 4, 6, 7, 8, 9])

    previous_rule: str | None = None
    planned: list[tuple[Any, ...]] = []
    for trial_index in range(1, n + 1):
        if previous_rule is None:
            task_rule = trial_rng.choice(["parity", "magnitude"])
            trial_type = "start"
        else:
            do_switch = trial_rng.random() < switch_p
            if do_switch:
                task_rule = "magnitude" if previous_rule == "parity" else "parity"
            else:
                task_rule = previous_rule
            trial_type = "switch" if task_rule != previous_rule else "repeat"

        target_digit = int(trial_rng.choice(digits))
        previous_rule = task_rule
        condition_id = f"{condition_name}_{task_rule}_{trial_type}_d{target_digit}_t{trial_index:03d}"
        planned.append(
            (
                condition_name,
                condition_id,
                int(trial_index),
                task_rule,
                trial_type,
                target_digit,
                trial_type == "switch",
                _sample_duration(timing_rng, fixation_duration, 0.45),
                _sample_duration(timing_rng, iti_duration, 0.45),
            )
        )

    if bool(enable_logging):
        logging.data(
            "[TaskSwitching] "
            f"generated_conditions={n} seed={base_seed} switch_probability={switch_p}"
        )
    return planned
