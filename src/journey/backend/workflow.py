import os

import networkx as nx
from dotenv import load_dotenv
from sqlalchemy import Row, Sequence

from journey.backend.dataLoader import DataLoader
from journey.backend.intermediate_artifacts import (
    DataBundle,
    DataSet,
    NodeCategory,
    WorkflowEdge,
    WorkflowNode,
)
from journey.backend.preprocessing import DataProcessor
from journey.backend.RDB import RDB

# --- Env Data ---
load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

class Workflow:

    def __init__(self) -> None:
        self._name: str = 'New Workflow'
        self._network = nx.DiGraph()
        self._dbManager = RDB(str(CONNECTION_STRING))
        self._dbRes: None | Sequence[Row] = None
        self._data_loader: DataLoader = DataLoader()
        self._data_processor = None
        self._run: dict[WorkflowNode, DataSet | DataBundle] = {}

    def initialize_data_processor(self):
        if self._data_processor == None:
            self._data_processor = DataProcessor(self._data_loader._data_set)

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
                self._run[node_id] = self._data_loader.load_sklearn_sample_dateset()._data_set
            elif node_category == NodeCategory.DATALOADER_SHOW_DATA_INFO:
                print(self._data_loader.show_dataframe_info())
            elif node_category == NodeCategory.DATALOADER_DATA_LOAD_CSV:
                self._run[node_id] = self._data_loader.read_csv()._data_set

            # print('-------Run Info-------\n', self._run)
            