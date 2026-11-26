# SPDX-FileCopyrightText: 2026 Johann Christensen
#
# SPDX-License-Identifier: MIT
"""Monotone ratchet on the per-module mutation score of mutmut.

Run `mutmut run` first. The script reads the `*.meta` files that mutmut
3.8.1 writes below `mutants/` (JSON, key `exit_code_by_key`: mutant name
to the exit code of its test run) and computes one score per source file
and per package (directory). A score is
`detected / (detected + undetected)`; `scripts.ratchet_counts` defines
how exit codes are classified. A module with pending mutants has an
incomplete run; it is an error, because its score is not comparable.

The baseline (default `mutation-baseline.json`) holds the best score
seen per module. Without `--update` the script fails (exit 1) when a
score is below its baseline. With `--update` it also writes the baseline
with every score raised to the new value; it never lowers one. Modules
without a baseline entry are added. A missing baseline file is created
(first run, exit 0).

Usage: `uv run python -m scripts.mutation_ratchet [--update]`.
"""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from scripts.ratchet_baseline import (
    format_report,
    load_baseline,
    ratchet,
    regressions,
    save_baseline,
)
from scripts.ratchet_counts import read_modules, scores, with_packages

EXIT_OK = 0
EXIT_REGRESSION = 1
EXIT_INCOMPLETE = 2
EXIT_NO_DATA = 3


def say(message: str) -> None:
    """Write one line to standard output.

    Args:
        message (str): The line, without newline.
    """
    sys.stdout.write(message + "\n")


def run(mutants_dir: Path, baseline_path: Path, *, update: bool) -> int:
    """Check, and optionally update, the baseline.

    Args:
        mutants_dir (Path): The `mutants/` directory written by `mutmut
            run`.
        baseline_path (Path): The baseline JSON.
        update (bool): Write the raised baseline if nothing regressed.

    Returns:
        int: The process exit code.
    """
    counts = with_packages(read_modules(mutants_dir))
    if not counts:
        say(f"No mutmut results below {mutants_dir}; run `mutmut run`.")
        return EXIT_NO_DATA
    incomplete = sorted(k for k, c in counts.items() if c.pending)
    if incomplete:
        say("Incomplete mutmut run (pending mutants): " + ", ".join(incomplete))
        return EXIT_INCOMPLETE
    current = scores(counts)
    stored = load_baseline(baseline_path)
    say(format_report(counts, stored or {}))
    if stored is None:
        save_baseline(baseline_path, current)
        say(f"No baseline found; created {baseline_path}.")
        return EXIT_OK
    worse = regressions(current, stored)
    for key, (old, new) in sorted(worse.items()):
        say(f"REGRESSION {key}: {new:.4f} < baseline {old:.4f}")
    if worse:
        return EXIT_REGRESSION
    if update:
        save_baseline(baseline_path, ratchet(current, stored))
        say(f"Updated {baseline_path}.")
    return EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    """Parse the command line and run the ratchet.

    Args:
        argv (Sequence[str] | None): Arguments without the program name;
            default `sys.argv`.

    Returns:
        int: The process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--mutants", type=Path, default=Path("mutants"))
    parser.add_argument("--baseline", type=Path, default=Path("mutation-baseline.json"))
    parser.add_argument(
        "--update",
        action="store_true",
        help="raise the baseline to the current scores (never lowers it)",
    )
    args = parser.parse_args(argv)
    return run(args.mutants, args.baseline, update=args.update)


if __name__ == "__main__":
    sys.exit(main())
