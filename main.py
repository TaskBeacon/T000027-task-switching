from __future__ import annotations

from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    count_down,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import Controller, run_trial


def _make_qa_trigger_runtime():
    return initialize_triggers(mock=True)


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def _parse_args(task_root: Path) -> TaskRunOptions:
    return parse_task_run_options(
        task_root=task_root,
        description="Run Task Switching Task in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _as_float(value) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def _as_int(value, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except Exception:
        return int(default)


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(sum(values) / len(values))


def _accuracy(rows: list[dict]) -> float:
    values = [row.get("is_correct", None) for row in rows if row.get("is_correct", None) is not None]
    if not values:
        return 0.0
    return float(sum(1 for value in values if _as_bool(value)) / len(values))


def _summarize_trials(trials: list[dict], fallback_score: int = 0) -> dict[str, float | int]:
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

    rt_values = [_as_float(row.get("decision_rt_s", None)) for row in responded]
    rt_values = [value for value in rt_values if value is not None]
    mean_rt_ms = _mean(rt_values) * 1000.0 if rt_values else 0.0

    switch_rt_values = [_as_float(row.get("decision_rt_s", None)) for row in switch_rows]
    switch_rt_values = [value for value in switch_rt_values if value is not None]
    mean_switch_rt_ms = _mean(switch_rt_values) * 1000.0 if switch_rt_values else 0.0

    repeat_rt_values = [_as_float(row.get("decision_rt_s", None)) for row in repeat_rows]
    repeat_rt_values = [value for value in repeat_rt_values if value is not None]
    mean_repeat_rt_ms = _mean(repeat_rt_values) * 1000.0 if repeat_rt_values else 0.0

    switch_cost_ms = mean_switch_rt_ms - mean_repeat_rt_ms if switch_rt_values and repeat_rt_values else 0.0

    score_end = int(fallback_score)
    for row in reversed(trials):
        if row.get("score_after", None) is not None:
            score_end = _as_int(row.get("score_after"), fallback_score)
            break

    net_score = sum(_as_int(row.get("score_delta", 0), 0) for row in trials)

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


def run(options: TaskRunOptions):
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))
    mode = options.mode

    ctx = None
    if mode in ("qa", "sim"):
        ctx = context_from_config(task_dir=task_root, config=cfg, mode=mode)
        sim_participant = "sim"
        if ctx.session is not None:
            sim_participant = str(ctx.session.participant_id or "sim")
        with runtime_context(ctx):
            _run_impl(mode=mode, output_dir=ctx.output_dir, cfg=cfg, participant_id=sim_participant)
    else:
        _run_impl(mode=mode, output_dir=None, cfg=cfg, participant_id="human")


def _run_impl(*, mode: str, output_dir: Path | None, cfg: dict, participant_id: str):
    if mode == "qa":
        subject_data = {"subject_id": "qa"}
    elif mode == "sim":
        subject_data = {"subject_id": participant_id}
    else:
        subform = SubInfo(cfg["subform_config"])
        subject_data = subform.collect()

    settings = TaskSettings.from_dict(cfg["task_config"])
    if mode in ("qa", "sim") and output_dir is not None:
        settings.save_path = str(output_dir)

    settings.add_subinfo(subject_data)

    if mode == "qa" and output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        settings.res_file = str(output_dir / "qa_trace.csv")
        settings.log_file = str(output_dir / "qa_psychopy.log")
        settings.json_file = str(output_dir / "qa_settings.json")

    settings.triggers = cfg["trigger_config"]
    if mode in ("qa", "sim"):
        trigger_runtime = _make_qa_trigger_runtime()
    else:
        trigger_runtime = initialize_triggers(cfg)

    win, kb = initialize_exp(settings)

    stim_bank = StimBank(win, cfg["stim_config"])
    if mode not in ("qa", "sim"):
        stim_bank = stim_bank.convert_to_voice("instruction_text")
    stim_bank = stim_bank.preload_all()

    settings.controller = cfg["controller_config"]
    settings.save_to_json()
    controller = Controller.from_dict(settings.controller)

    trigger_runtime.send(settings.triggers.get("exp_onset"))

    instruction = StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get("instruction_text")
    )
    if mode not in ("qa", "sim"):
        instruction.add_stim(stim_bank.get("instruction_text_voice"))
    instruction.wait_and_continue()

    all_data: list[dict] = []
    total_blocks = int(getattr(settings, "total_blocks", 1))

    for block_i in range(total_blocks):
        controller.start_block(block_i)
        if mode not in ("qa", "sim"):
            count_down(win, 3, color="white")

        block = (
            BlockUnit(
                block_id=f"block_{block_i}",
                block_idx=block_i,
                settings=settings,
                window=win,
                keyboard=kb,
            )
            .generate_conditions()
            .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
            .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
            .run_trial(
                partial(
                    run_trial,
                    stim_bank=stim_bank,
                    controller=controller,
                    trigger_runtime=trigger_runtime,
                    block_id=f"block_{block_i}",
                    block_idx=block_i,
                )
            )
            .to_dict(all_data)
        )

        block_summary = _summarize_trials(block.get_all_data(), fallback_score=int(controller.current_score))

        if block_i < (total_blocks - 1):
            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=total_blocks,
                    accuracy=block_summary["accuracy"],
                    switch_accuracy=block_summary["switch_accuracy"],
                    repeat_accuracy=block_summary["repeat_accuracy"],
                    timeout_count=block_summary["timeout_count"],
                    mean_rt_ms=block_summary["mean_rt_ms"],
                    switch_cost_ms=block_summary["switch_cost_ms"],
                    score_end=block_summary["score_end"],
                    net_score=block_summary["net_score"],
                )
            ).wait_and_continue()

    overall = _summarize_trials(all_data, fallback_score=int(controller.current_score))

    StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get_and_format(
            "good_bye",
            total_trials=len(all_data),
            accuracy=overall["accuracy"],
            switch_accuracy=overall["switch_accuracy"],
            repeat_accuracy=overall["repeat_accuracy"],
            timeout_count=overall["timeout_count"],
            mean_rt_ms=overall["mean_rt_ms"],
            mean_switch_rt_ms=overall["mean_switch_rt_ms"],
            mean_repeat_rt_ms=overall["mean_repeat_rt_ms"],
            switch_cost_ms=overall["switch_cost_ms"],
            score_end=overall["score_end"],
            net_score=overall["net_score"],
        )
    ).wait_and_continue(terminate=True)

    trigger_runtime.send(settings.triggers.get("exp_end"))

    pd.DataFrame(all_data).to_csv(settings.res_file, index=False)

    trigger_runtime.close()
    core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = _parse_args(task_root)
    run(options)


if __name__ == "__main__":
    main()
