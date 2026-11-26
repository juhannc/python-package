# SPDX-FileCopyrightText: 2026 Johann Christensen
#
# SPDX-License-Identifier: MIT
"""Compare scores with the stored baseline; only ever raise it."""

import json
from collections.abc import Mapping
from pathlib import Path

from scripts.ratchet_counts import Counts, scores

TOLERANCE = 1e-12


def regressions(
    current: Mapping[str, float], baseline: Mapping[str, float]
) -> dict[str, tuple[float, float]]:
    """Find the modules whose score is below the baseline.

    Args:
        current (Mapping[str, float]): Current score per module.
        baseline (Mapping[str, float]): Best known score per module.

    Returns:
        dict[str, tuple[float, float]]: Module key to (baseline,
            current), for every decrease.
    """
    return {
        key: (baseline[key], score)
        for key, score in current.items()
        if key in baseline and score < baseline[key] - TOLERANCE
    }


def ratchet(
    current: Mapping[str, float], baseline: Mapping[str, float]
) -> dict[str, float]:
    """Raise the baseline to the current scores, never lowering it.

    Args:
        current (Mapping[str, float]): Current score per module.
        baseline (Mapping[str, float]): Best known score per module.

    Returns:
        dict[str, float]: The element-wise maximum; baseline-only
            modules are kept.
    """
    return {
        key: max(current.get(key, 0.0), baseline.get(key, 0.0))
        for key in sorted(current.keys() | baseline.keys())
    }


def load_baseline(path: Path) -> dict[str, float] | None:
    """Read the baseline file.

    Args:
        path (Path): The baseline JSON.

    Returns:
        dict[str, float] | None: Module key to score, or `None` if the
            file does not exist.
    """
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))["scores"]


def save_baseline(path: Path, baseline: Mapping[str, float]) -> None:
    """Write the baseline file (LF line endings, sorted keys).

    Args:
        path (Path): The baseline JSON.
        baseline (Mapping[str, float]): Module key to score.
    """
    text = json.dumps({"scores": baseline}, indent=2, sort_keys=True)
    path.write_bytes((text + "\n").encode("utf-8"))


def format_report(counts: Mapping[str, Counts], baseline: Mapping[str, float]) -> str:
    """Render the scores next to the baseline as a text table.

    Args:
        counts (Mapping[str, Counts]): Module key to counts.
        baseline (Mapping[str, float]): Best known score per module (may
            be empty).

    Returns:
        str: One line per scored module.
    """
    lines = []
    for key, score in sorted(scores(counts).items()):
        old = f"{baseline[key]:.4f}" if key in baseline else "new"
        c = counts[key]
        lines.append(
            f"{key}: {score:.4f} (baseline {old}; {c.detected}/{c.tested} detected)"
        )
    return "\n".join(lines)
