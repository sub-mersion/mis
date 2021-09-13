#!/usr/bin/env python3
#
# Recoding the shift scheduling script from google repo
# https://github.com/google/or-tools/blob/master/examples/python/shift_scheduling_sat.py
# with
# 1. user / other program input (so that it's a standalone script)
# 2. custom french rules regarding "gardes" and "astreintes".
"""Solves a scheduling problem for physicians in an hospital service."""
import argparse
from ortools.sat.python import cp_model


def main(args: argparse.Namespace) -> None:
    n_intern = args.interns
    n_weeks = args.weeks
    n_days = 7 * args.weeks
    n_lines = args.lines

    print("Interns: {} Days: {} Lines: {}".format(n_intern, n_days, n_lines))
    print()

    all_interns = range(n_intern)
    all_days = range(n_days)
    all_lines = range(n_lines)

    model = cp_model.CpModel()

    work: dict[cp_model.IntVar] = {}
    for n in all_interns:
        for d in all_days:
            for l in all_lines:
                work[(n, d, l)] = model.NewBoolVar(f"work_{n}d{d}l{l}")

    # Each line on each day is occupied by an intern.
    for l in all_lines:
        for d in all_days:
            model.Add(sum([work[(n, d, l)] for n in all_interns]) == 1)

    # Each intern is on at most one line per day.
    for n in all_interns:
        for d in all_days:
            model.Add(sum([work[(n, d, l)] for l in all_lines]) <= 1)

    # Forbid any sequence of work longer than 4: on a sliding window of 5 days,
    # there has to be at least one day off.
    worked_days_hard_max = 4
    for n in all_interns:
        for start in range(n_days - worked_days_hard_max):
            model.Add(
                sum(
                    [
                        work[(n, d, l)]
                        for d in range(start, start + worked_days_hard_max + 1)
                        for l in all_lines
                    ]
                )
                <= worked_days_hard_max
            )

    # Forbid any sequence of rest longer than 3: on a sliding window of 4 days,
    # there has to be at least one worked day.
    rest_days_hard_max = 3
    for n in all_interns:
        for start in range(n_days - rest_days_hard_max):
            model.Add(
                sum(
                    [
                        work[(n, d, l)]
                        for d in range(start, start + rest_days_hard_max + 1)
                        for l in all_lines
                    ]
                )
                >= 1
            )

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        header = " " * 12
        for _ in range(n_weeks):
            header += "M T W T F S S "
        print(header)

        for n in all_interns:
            schedule = ""
            for d in all_days:
                working = False
                for l in all_lines:
                    if solver.BooleanValue(work[(n, d, l)]):
                        schedule += str(l) + " "
                        working = True
                if not working:
                    schedule += "_ "
            print("Worker {}:   {}".format(n, schedule))
        print()

        print(header)
        for l in all_lines:
            schedule = ""
            for d in all_days:
                for n in all_interns:
                    if solver.BooleanValue(work[(n, d, l)]):
                        schedule += str(n) + " "
            print("Line {}:     {}".format(l, schedule))

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=True)
    parser.add_argument(
        "-v", "--verbose", help="set verbose output", action="store_true"
    )
    parser.add_argument("interns", help="number of interns", type=int)
    parser.add_argument("weeks", help="number of weeks", type=int)
    parser.add_argument("lines", help="number of work lines", type=int)
    args = parser.parse_args()
    main(args)
