# SPDX-FileCopyrightText: 2026 Johann Christensen
#
# SPDX-License-Identifier: MIT
"""Read mutmut `.meta` files and map exit codes to mutant counts.

The exit codes are classified as in `mutmut.stats.status_by_exit_code`:

* detected: killed (1, 3), timeout (36, 24, -24, 152, 255), segfault
    (-11, -9) and caught by type check (37).
* undetected: survived (0), no tests (5, 33), suspicious (35) and every
    unknown exit code.
* excluded: skipped (34), which counts for neither side.
* pending: not checked (`null`) and interrupted by the user (2).
"""

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

DETECTED_CODES = frozenset({1, 3, 36, 24, -24, 152, 255, -11, -9, 37})
EXCLUDED_CODES = frozenset({34})
PENDING_CODES = frozenset({None, 2})


@dataclass(frozen=True)
class Counts:
    """Mutant counts of one module.

    Attributes:
        detected (int): Mutants caught (killed, timed out, crashed or
            type-checked).
        undetected (int): Mutants caught (killed, timed out, crashed or
            type-checked).
        pending (int): Mutants not yet checked or interrupted.
        tested (int): Number of mutants that enter the score.
        score (float): Detected fraction of tested mutants (1.0 if
            none).
    """

    detected: int = 0
    undetected: int = 0
    pending: int = 0

    def __add__(self, other: "Counts") -> "Counts":
        """Add two counts.

        Args:
            other ('Counts'): The counts to add.

        Returns:
            'Counts': The component-wise sum.
        """
        return Counts(
            self.detected + other.detected,
            self.undetected + other.undetected,
            self.pending + other.pending,
        )

    @property
    def tested(self) -> int:
        """Number of mutants that enter the score."""
        return self.detected + self.undetected

    @property
    def score(self) -> float:
        """Detected fraction of tested mutants (1.0 if none)."""
        return self.detected / self.tested if self.tested else 1.0


def classify(exit_code: int | None) -> Counts:
    """Map the exit code of one mutant to a count.

    Args:
        exit_code (int | None): The mutmut exit code, `None` if not
            checked.

    Returns:
        Counts: A `Counts` with exactly one mutant in its category.
    """
    if exit_code in PENDING_CODES:
        return Counts(pending=1)
    if exit_code in EXCLUDED_CODES:
        return Counts()
    if exit_code in DETECTED_CODES:
        return Counts(detected=1)
    return Counts(undetected=1)


def count_meta(meta: Mapping[str, Mapping[str, int | None]]) -> Counts:
    """Count the mutants of one parsed `.meta` file.

    Args:
        meta (Mapping[str, Mapping[str, int | None]]): The JSON content
            of the file.

    Returns:
        Counts: The summed counts over `exit_code_by_key`.
    """
    total = Counts()
    for code in meta.get("exit_code_by_key", {}).values():
        total += classify(code)
    return total


def read_modules(mutants_dir: Path) -> dict[str, Counts]:
    """Read the counts per source file from mutmut's `.meta` files.

    Args:
        mutants_dir (Path): The `mutants/` directory written by `mutmut
            run`.

    Returns:
        dict[str, Counts]: Posix source path to counts.
    """
    modules = {}
    for meta_path in sorted(mutants_dir.rglob("*.meta")):
        relative = PurePosixPath(meta_path.relative_to(mutants_dir).as_posix())
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        modules[str(relative.with_suffix(""))] = count_meta(meta)
    return modules


def with_packages(modules: Mapping[str, Counts]) -> dict[str, Counts]:
    """Add the sum over each directory to the per-file counts.

    Args:
        modules (Mapping[str, Counts]): Source path to counts.

    Returns:
        dict[str, Counts]: The input plus one entry per parent directory
            of a file.
    """
    result = dict(modules)
    for path, counts in modules.items():
        package = str(PurePosixPath(path).parent)
        result[package] = result.get(package, Counts()) + counts
    return result


def scores(counts: Mapping[str, Counts]) -> dict[str, float]:
    """Select the modules that have a score.

    Args:
        counts (Mapping[str, Counts]): Module key to counts.

    Returns:
        dict[str, float]: Module key to score, without modules that have
            no tested mutant.
    """
    return {key: c.score for key, c in counts.items() if c.tested}
