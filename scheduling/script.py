#!/usr/bin/env python3
"""My take on google nurse shifts scehduling problem example."""
from ortools.sat.python import cp_model


def main():
    n_interns = 4
    n_shifts_by_day = 3
    n_days = 5

    all_interns = range(n_interns)
    all_shifts_by_day = range(n_shifts_by_day)
    all_days = range(n_days)

    model = cp_model.CpModel()

    shifts = {}
    for n in all_interns:
        for d in all_days:
            for s in all_shifts_by_day:
                shifts[(n, d, s)] = model.NewBoolVar(f"shift_n{n}d{d}s{s}")

    # Every shift has one and only one assigned intern
    for d in all_days:
        for s in all_shifts_by_day:
            model.Add(sum([shifts[(n, d, s)] for n in all_interns]) == 1)

    # Every intern has at most one shift per day
    for n in all_interns:
        for d in all_days:
            model.Add(sum([shifts[(n, d, s)] for s in all_shifts_by_day]) <= 1)

    # Distributing the shifts evenly
    min_shifts_per_intern = (n_shifts_by_day * n_days) // n_interns
    for n in all_interns:
        num_shifts_worked = 0
        for d in all_days:
            for s in all_shifts_by_day:
                num_shifts_worked += shifts[(n, d, s)]
        model.Add(min_shifts_per_intern <= num_shifts_worked)

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0

    a_few_sols = range(5)
    solution_printer = PartialSolutionPrinter(
        shifts, n_interns, n_shifts_by_day, n_days, a_few_sols
    )
    solver.SearchForAllSolutions(model, solution_printer)

    print()
    print("Statistics")
    print("  - conflicts       : {}".format(solver.NumConflicts()))
    print("  - branches        : {}".format(solver.NumBranches()))
    print("  - wall time       : {} s".format(solver.WallTime()))
    print("  - solutions found : {}".format(solution_printer.solution_count()))


class PartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solution"""

    def __init__(self, shifts, n_interns, n_shifts, n_days, sols):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._n_interns = n_interns
        self._n_days = n_days
        self._n_shifts = n_shifts
        self._solutions = set(sols)
        self._solution_count = 0

    def on_solution_callback(self):
        if self._solution_count in self._solutions:
            print(f"Solution {self._solution_count}")
            for d in range(self._n_days):
                print(f"Day {d}")
                for n in range(self._n_interns):
                    is_working = False
                    for s in range(self._n_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print(f"\tIntern {n} works on shift {s}")
                    if not is_working:
                        print(f"\tIntern {n} does not work")
            print()
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count


if __name__ == "__main__":
    main()
