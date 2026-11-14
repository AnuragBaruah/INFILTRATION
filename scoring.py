"""Per-level completion scoring and persistent best-run records."""
from __future__ import annotations

import json
from pathlib import Path


SCORE_FILE = Path(__file__).resolve().with_name("Level-High-Scores.json")


def format_time(seconds: int | float) -> str:
    total = max(0, int(seconds))
    return f"{total // 60:02d}:{total % 60:02d}"


def calculate_result(level_name: str, elapsed_seconds: int | float,
                     ghosts_killed: int, patrols_killed: int,
                     starting_health: int, health_remaining: int) -> dict:
    elapsed = max(0, int(elapsed_seconds))
    start_hp = max(1, int(starting_health))
    remaining = min(start_hp, max(0, int(health_remaining)))
    lost = start_hp - remaining
    time_bonus = max(0, 3600 - elapsed * 8)
    combat_bonus = max(0, int(ghosts_killed)) * 450 + max(0, int(patrols_killed)) * 200
    health_bonus = remaining * 25
    return {
        "level": level_name,
        "time_seconds": elapsed,
        "ghosts_killed": max(0, int(ghosts_killed)),
        "patrols_killed": max(0, int(patrols_killed)),
        "starting_health": start_hp,
        "health_lost": lost,
        "health_remaining": remaining,
        "time_bonus": time_bonus,
        "combat_bonus": combat_bonus,
        "health_bonus": health_bonus,
        "score": 1000 + time_bonus + combat_bonus + health_bonus,
    }


def _load_records() -> dict:
    try:
        with SCORE_FILE.open("r", encoding="utf-8") as f:
            records = json.load(f)
        return records if isinstance(records, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def record_result(result: dict) -> dict:
    records = _load_records()
    old_best = records.get(result["level"], {})
    if not isinstance(old_best, dict):
        old_best = {}
    is_new_record = result["score"] > int(old_best.get("score", -1))
    if is_new_record:
        best = {key: result[key] for key in (
            "score", "time_seconds", "ghosts_killed", "patrols_killed",
            "starting_health", "health_lost", "health_remaining",
        )}
        records[result["level"]] = best
        temp = SCORE_FILE.with_suffix(".json.tmp")
        with temp.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, sort_keys=True)
        temp.replace(SCORE_FILE)
    else:
        best = old_best
    result = dict(result)
    result["is_new_record"] = is_new_record
    result["best"] = dict(best)
    return result
