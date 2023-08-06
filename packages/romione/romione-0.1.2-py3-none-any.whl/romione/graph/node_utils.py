import yaml
import sympy as sp

from romione.graph.compute_utils import parse_vector
from romione.graph.Node import Node


def get_node_values(graph, nodes=[]):
    node_values = []
    if not nodes:
        nodes = graph.nodes
    elif isinstance(nodes, str):
        nodes = [nodes]

    for n in nodes:
        node = graph.nodes[n]["node"]
        if isinstance(node.name, sp.Symbol):
            node_values.append((node.name.name, node.value))

    return node_values


def set_node_values(graph, values=0):
    for n in graph.nodes:
        node = graph.nodes[n]["node"]

        if isinstance(values, dict):
            if isinstance(node.name, sp.Symbol):
                if node.name.name in values:
                    node.value = parse_vector(values[node.name.name])

        else:
            node.value = parse_vector(values)

    return graph


def update_graph_from_yaml(
    graph, yaml_file, symbols_key="Symbols", eqns_key="Equations"
):

    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    for k, v in data[symbols_key].items():
        graph.add_node(k, node=Node(name=v, graph=graph))

    for k, v in data[eqns_key].items():
        graph.add_node(k, node=Node(name=k, eqn=v, graph=graph))

    return graph
