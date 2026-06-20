from __future__ import annotations

from functools import partial
from psyflow import StimUnit, next_trial_id, resolve_deadline, set_trial_context

from .utils import as_dict, parse_task_switching_condition, task_switching_rule_profile


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one cue-based task-switching trial."""
    parsed = parse_task_switching_condition(condition)
    condition_name = parsed["condition"]
    trial_id = next_trial_id()
    trial_index = int(parsed["trial_index"]) if int(parsed["trial_index"]) > 0 else int(trial_id)
    block_idx_val = int(block_idx) if block_idx is not None else 0

    task_rule = str(parsed["task_rule"]).strip().lower()
    trial_type = str(parsed["trial_type"]).strip().lower()
    target_digit = int(parsed["target_digit"])

    left_key = str(getattr(settings, "left_key", "f")).strip().lower()
    right_key = str(getattr(settings, "right_key", "j")).strip().lower()
    response_keys = [left_key, right_key]

    trial_type_names = as_dict(getattr(settings, "trial_type_names", {}))
    trial_type_label = str(trial_type_names.get(trial_type, trial_type))

    profile = task_switching_rule_profile(task_rule, target_digit, left_key, right_key, settings)

    fixation_duration = (
        float(parsed["fixation_duration"])
        if parsed["fixation_duration"] is not None
        else float(resolve_deadline(settings.fixation_duration) or 0.45)
    )
    cue_duration = float(settings.cue_duration)
    decision_deadline = float(settings.decision_deadline)
    feedback_duration = float(settings.feedback_duration)
    iti_duration = (
        float(parsed["iti_duration"])
        if parsed["iti_duration"] is not None
        else float(resolve_deadline(settings.iti_duration) or 0.45)
    )

    current_score = int(getattr(controller, "current_score", 0))
    trial_data = {
        "condition": condition_name,
        "trial_id": trial_id,
        "scheduled_trial_index": trial_index,
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "condition_id": parsed["condition_id"],
        "task_rule": profile["rule"],
        "trial_type": trial_type,
        "trial_type_cn": trial_type_label,
        "target_digit": target_digit,
        "switch_trial": bool(parsed["switch_trial"]),
        "left_key": left_key,
        "right_key": right_key,
        "left_label_cn": profile["left_label"],
        "right_label_cn": profile["right_label"],
        "rule_name_cn": profile["rule_name"],
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=resolve_deadline(fixation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "fixation",
            "task_rule": profile["rule"],
            "trial_type": trial_type,
            "target_digit": target_digit,
            "block_idx": block_idx_val,
        },
        stim_id="fixation",
    )
    fixation.show(
        duration=fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    cue_stim_id = f"cue_{profile['rule']}"
    cue = make_unit(unit_label="cue")
    cue.add_stim(stim_bank.get("cue_title"))
    cue.add_stim(stim_bank.get_and_format("score_text", current_score=current_score))
    cue.add_stim(stim_bank.get(cue_stim_id))
    cue.add_stim(stim_bank.get_and_format("trial_type_tag", trial_type_cn=trial_type_label))
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="cue",
        deadline_s=resolve_deadline(cue_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "cue",
            "task_rule": profile["rule"],
            "trial_type": trial_type,
            "trial_type_cn": trial_type_label,
            "target_digit": target_digit,
            "current_score": current_score,
            "block_idx": block_idx_val,
        },
        stim_id=f"cue_title+score_text+{cue_stim_id}+trial_type_tag",
    )
    cue.show(
        duration=cue_duration,
        onset_trigger=settings.triggers.get("cue_onset"),
    ).to_dict(trial_data)

    decision = make_unit(unit_label="decision")
    decision.add_stim(stim_bank.get_and_format("score_text", current_score=current_score))
    decision.add_stim(stim_bank.rebuild("target_digit", text=str(target_digit)))
    decision.add_stim(stim_bank.get_and_format("rule_prompt", rule_name_cn=profile["rule_name"]))
    decision.add_stim(
        stim_bank.get_and_format(
            "key_hint",
            left_key=left_key.upper(),
            right_key=right_key.upper(),
            left_label_cn=profile["left_label"],
            right_label_cn=profile["right_label"],
        )
    )
    set_trial_context(
        decision,
        trial_id=trial_id,
        phase="decision",
        deadline_s=resolve_deadline(decision_deadline),
        valid_keys=response_keys,
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "decision",
            "task_rule": profile["rule"],
            "trial_type": trial_type,
            "target_digit": target_digit,
            "left_key": left_key,
            "right_key": right_key,
            "correct_key": profile["correct_key"],
            "current_score": current_score,
            "block_idx": block_idx_val,
        },
        stim_id="score_text+target_digit+rule_prompt+key_hint",
    )
    decision.capture_response(
        keys=response_keys,
        duration=decision_deadline,
        onset_trigger=settings.triggers.get("decision_onset"),
        response_trigger={
            left_key: settings.triggers.get("choice_left"),
            right_key: settings.triggers.get("choice_right"),
        },
        timeout_trigger=settings.triggers.get("choice_timeout"),
    )
    decision.to_dict(trial_data)

    response_key = str(decision.get_state("response", "")).strip().lower()
    timed_out = response_key not in response_keys

    is_correct: bool | None = None if timed_out else (response_key == profile["correct_key"])
    score_update = controller.apply_score(is_correct)

    if timed_out:
        feedback_stim_id = "feedback_timeout"
        feedback_onset = "feedback_timeout"
        predicted_label = "none"
        predicted_category = "none"
        feedback_stim = stim_bank.get_and_format(
            feedback_stim_id,
            rule_name_cn=profile["rule_name"],
            correct_category_cn=profile["correct_label"],
            score_after=score_update["score_after"],
        )
    else:
        feedback_stim_id = "feedback_correct" if bool(is_correct) else "feedback_incorrect"
        feedback_onset = feedback_stim_id
        if response_key == left_key:
            predicted_label = profile["left_label"]
            predicted_category = "left"
        else:
            predicted_label = profile["right_label"]
            predicted_category = "right"
        feedback_stim = stim_bank.get_and_format(
            feedback_stim_id,
            predicted_category_cn=predicted_label,
            correct_category_cn=profile["correct_label"],
            score_delta=score_update["score_delta"],
            score_after=score_update["score_after"],
        )

    feedback = make_unit(unit_label="feedback").add_stim(feedback_stim)
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="feedback",
        deadline_s=resolve_deadline(feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "feedback",
            "task_rule": profile["rule"],
            "trial_type": trial_type,
            "target_digit": target_digit,
            "response_key": response_key,
            "timed_out": timed_out,
            "is_correct": is_correct,
            "score_after": score_update["score_after"],
            "block_idx": block_idx_val,
        },
        stim_id=feedback_stim_id,
    )
    feedback.show(
        duration=feedback_duration,
        onset_trigger=settings.triggers.get(feedback_onset),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="inter_trial_interval").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=resolve_deadline(iti_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={"stage": "inter_trial_interval", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    rt = decision.get_state("rt", None)
    key_press = decision.get_state("key_press", None)
    rt_s = float(rt) if isinstance(rt, (int, float)) else None

    trial_data.update(
        {
            "response_key": response_key if not timed_out else "",
            "decision_response": response_key if not timed_out else "",
            "decision_key_press": bool(key_press) if key_press is not None else not timed_out,
            "decision_rt": rt_s,
            "decision_rt_s": rt_s,
            "decision_timed_out": bool(timed_out),
            "is_correct": bool(is_correct) if is_correct is not None else None,
            "correct_key": profile["correct_key"],
            "correct_category": profile["correct_category"],
            "correct_category_cn": profile["correct_label"],
            "predicted_category": predicted_category,
            "predicted_category_cn": predicted_label,
            "score_before": score_update["score_before"],
            "score_after": score_update["score_after"],
            "score_delta": score_update["score_delta"],
        }
    )

    controller.record_trial(trial_data)
    return trial_data
