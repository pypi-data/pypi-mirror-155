import sympy as sp
from sympy import Symbol
from sympy.solvers import solve
from sympy.parsing.sympy_parser import parse_expr

from romione.graph.compute_utils import parse_vector
from romione.graph.heuristics import complexity


class Node(object):
    def __init__(
        self,
        name="s",
        value=0,
        eqn=None,
        graph=None,
    ):

        self.name = name if eqn else Symbol(name)
        self.value = parse_vector(value)
        self.graph = graph
        self.eqn = eqn

        if eqn is not None:
            eqn = [i.strip() for i in eqn.split("=")]
            self.lhs = parse_expr(eqn[0])
            self.rhs = parse_expr(eqn[1])

        self.add_edges()

    def add_edges(self):
        if self.graph is not None:
            for s in set.union(self.lhs.free_symbols, self.rhs.free_symbols):
                self.graph.add_edge(s.name, self.name)


    def get_complexity(self):
        r"""Heuristics based complexity estimation to prioritize equations for 
        solving in terms of target symbols."""

        complexity_value = 0
        if self.eqn is not None:
            expr = self.lhs - self.rhs
            tgt_symbols = [s for s in expr.free_symbols if self.graph.nodes[s.name]["node"].value is None]
            complexity_value += complexity(expr, tgt_symbols)

        return complexity_value

    def solve(self):
        if self.eqn is not None:
            solve_for = []
            eqn = self.lhs - self.rhs

            for i in self.graph.pred[self.name]:
                node = self.graph.nodes[i]["node"]
                if isinstance(node.name, Symbol):
                    if node.value is None:
                        solve_for.append(node.name)
                    else:
                        eqn = eqn.subs(node.name, node.value)

            res = solve(eqn, *solve_for)

            return res

    def propagate(self):
        raise NotImplementedError
