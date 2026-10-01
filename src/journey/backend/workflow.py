from dataclasses import dataclass

import matplotlib.pyplot as plt
import networkx as nx

from journey.backend.intermediate_artifacts import (
    WorkflowEdge,
    WorkflowNode,
)


class Workflow:

    def __init__(self) -> None:
        self._name: str = 'New Workflow'
        self._network = nx.Graph()

    def create_graph(self, nodes: list[WorkflowNode], edges: list[WorkflowEdge]):
        for node in nodes:
            self._network.add_node(node.id, type=node.type)
        for edge in edges:
            self._network.add_edge(edge.source, edge.target)            
        
        nx.draw(self._network, with_labels=False)
        plt.show()