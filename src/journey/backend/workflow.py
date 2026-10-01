import networkx as nx

from journey.backend.dataLoader import DataLoader
from journey.backend.intermediate_artifacts import (
    NodeCategory,
    WorkflowEdge,
    WorkflowNode,
)


class Workflow:

    def __init__(self) -> None:
        self._name: str = 'New Workflow'
        self._network = nx.DiGraph()
        self._data_loader = DataLoader()

    def create_graph(self, nodes: list[WorkflowNode], edges: list[WorkflowEdge]):
        G = nx.DiGraph()
        for node in nodes:
            G.add_node(node.id, type=node.type, category=node.data.get("category") if node.data else None)
        for edge in edges:
            G.add_edge(edge.source, edge.target)

        is_diag: bool = nx.is_directed_acyclic_graph(G) 
        if is_diag:
            self._network = G

            print("Graph created with nodes and edges.")
            print("Nodes:", self._network.nodes(data=True))
            print("Edges:", self._network.edges(data=True))
    
            order = nx.topological_sort(self._network)
    
            print("topological sort", list(order))

            self.exceution()

        # nx.draw(self._network, with_labels=False)
        # plt.show()

    def exceution(self):
        network = self._network
        order = nx.topological_sort(network)

        print('---------Execution----------')
        for node_id in order:
            node_category = network.nodes[node_id]['category']
            print(node_id, node_category)

            if node_category == NodeCategory.DATALOADER_DATA_LOAD_SKLEARN:
                self._data_loader.load_sklearn_sample_dateset()
            elif node_category == NodeCategory.DATALOADER_SHOW_DATA_INFO:
                print(self._data_loader.show_dataframe_info())
            elif node_category == NodeCategory.DATALOADER_DATA_LOAD_CSV:
                self._data_loader.read_csv()
