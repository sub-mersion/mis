# Solving the Maximum Independent Set (MIS) problem

![MIS on a graph, from https://arxiv.org/pdf/2006.11190.pdf](image.png)

MIS can be expressed as a linear programming problem.

We demonstrate in `mis_julia.ipynb` how to solve the MIS in Julia using the
[JuMP](https://jump.dev) library, while the script `mis_solver.py` uses the
[ortools](https://developers.google.com/optimization) library to solves the MIS
on the graph given in input.

## Note

Linear programming is not the canonical approach to solve the MIS, and has
greater complexity. Specialized libraries use either an exact algorithm, or give
an approximate solution by sampling in maximal independent sets:

- [igraph](https://igraph.org) (python, C): [exact](https://igraph.org/python/doc/api/igraph._igraph.GraphBase.html#maximal_independent_vertex_sets), with [this](https://epubs.siam.org/doi/abs/10.1137/0206036) algorithm which gets _all_ the maximal independent sets.
- [networkx](https://networkx.org/documentation/stable/index.html) (python):
  approximate, see [this method](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.approximation.clique.maximum_independent_set.html#networkx.algorithms.approximation.clique.maximum_independent_set)
- [mis](https://github.com/Ravenlocke/mis) (Rust): approximate, faster (?) than networkx
- [LightGraphs](https://github.com/JuliaGraphs/LightGraphs.jl) (Julia): exact
