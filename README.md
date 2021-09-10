# Solving the Maximum Independent Set (MIS) problem

![MIS on a graph, from https://arxiv.org/pdf/2006.11190.pdf](image.png)

MIS can be expressed as a linear programming problem.

We demonstrate in `mis_julia.ipynb` how to solve the MIS in Julia using the
[JuMP](https://jump.dev) library, while the script `mis_solver.py` uses the
[ortools](https://developers.google.com/optimization) library to solves the MIS
on the graph given in input.
