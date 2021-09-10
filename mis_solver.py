#!/usr/bin/env python3
"""
This script solves a Maximum Indepent Set (MIS) problem as a linear programming
problem using the ortools library.
"""

import sys, json
from argparse import ArgumentParser
from ortools.linear_solver import pywraplp


class NegativeNodeNumberErr(Exception):
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return f"number of node is negative: {self.n}"


class ImpossibleEdgeErr(Exception):
    """
    ImpossibleEdge is an exception for edges between at least one unexisting
    node, that is of index out of [0, n-1].
    """

    def __init__(self, i, j, n):
        self.i = i
        self.j = j
        self.n = n

    def __str__(self):
        return f"impossible edge: ({self.i}, {self.j}) (max node label is {self.n-1})"


def solve(args):
    """
    solve takes parsed args from the command line and try to solve the MIS on
    the given graph.

    Return:
        a solution as a list of vertices if found, otherwise notify by a string.
    """

    solver = pywraplp.Solver.CreateSolver("SCIP")
    solver.SetTimeLimit(args.time_limit)

    n = 0
    edges = []

    try:
        if args.json:
            n, edges = parse_file_as_json(args.file)
        else:
            n, edges = parse_file(args.file)
    except OSError as err:
        sys.exit("cannot open file {}: {}".format(args.file, err))
    except (ValueError, ImpossibleEdgeErr, NegativeNodeNumberErr) as err:
        sys.exit("cannot parse file {}: {}".format(args.file, err))

    if args.verbose:
        print("{} parsed succesfully".format(args.file))
        print(f"number of nodes: {n}")
        print("edges:")
        edges.sort()
        for e in edges:
            print(f"({e[0]}, {e[1]})")

    # Set up the MIS problem
    x = {}
    for i in range(n):
        x[i] = solver.IntVar(0, 1, f"x_{i}")

    for e in edges:
        solver.Add(x[e[0]] + x[e[1]] <= 1)

    solver.Maximize(sum(x[i] for i in range(n)))

    if args.verbose:
        solver.EnableOutput()

    # Optimize!
    if solver.Solve() == pywraplp.Solver.OPTIMAL:
        print([i for i in range(n) if x[i].solution_value() > 0])
    else:
        print("The problem does not have an optimal solution")


def parse_file(filename):
    """
    parse_file parses graph file. The first line is expected to be an integer
    specifying n, the number of node of the graph, and following lines are edges
    between the nodes labels from 0 to n-1, separated by spaces.

    Example:
        4
        0 1
        0 2
        1 3

    Raises:
        ImpossibleEdgeErr if an edge refers to a node outside [0,n-1].

    Return:
        the number of nodes, and the edges as a list of 2-tuples.
    """
    n = 0
    edges = []
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if i == 0:
                n = int(line)
            else:
                i, j = [int(s) for s in line.split(" ", 1)]
                if i < 0 or i >= n or j < 0 or j >= n:
                    raise ImpossibleEdgeErr(i, j, n)
                edges.append((i, j))
    if n <= 0:
        raise NegativeNodeNumberErr(n)
    return n, edges


def parse_file_as_json(filename):
    """
    parse_file_as_json parse a graph given a json file.

    Example:
        {"n_node": 4, "edges": [ [0,1], [0,2], [1,3] ]}

    Return:
        the number of nodes, and the edges as a list of 2-item lists.
    """
    with open(filename, "r") as f:
        graph = json.load(f)
    if graph["n_nodes"] <= 0:
        raise NegativeNodeNumberErr(graph["n_nodes"])
    for e in graph["edges"]:
        if e[0] < 0 or e[0] >= graph["n_nodes"] or e[1] < 0 or e[1] >= graph["n_nodes"]:
            raise ImpossibleEdgeErr(e[0], e[1], graph["n_nodes"])
    return graph["n_nodes"], graph["edges"]


if __name__ == "__main__":
    parser = ArgumentParser("mis_solver.py", description=__doc__)
    parser.add_argument("file", help="read the given file and parse it as a graph")
    parser.add_argument(
        "--json", help="parse the input file as a JSON file", action="store_true"
    )
    parser.add_argument(
        "-t", "--time_limit", type=int, help="set the solver time limit", default=15
    )
    parser.add_argument(
        "-v", "--verbose", help="set the solver in verbose mode", action="store_true"
    )
    args = parser.parse_args()
    solve(args)
