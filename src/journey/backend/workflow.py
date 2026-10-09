import os

import networkx as nx
from dotenv import load_dotenv

from journey.backend.dataLoader import DataLoader
from journey.backend.intermediate_artifacts import (
    DataSet,
    NodeCategory,
    WorkflowEdge,
    WorkflowNode,
)
from journey.backend.RDB import RDB

# --- Env Data ---
load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

class Workflow:

    def __init__(self) -> None:
        self._name: str = 'New Workflow'
        self._network = nx.DiGraph()
        # self._dbManager = RDB(str(CONNECTION_STRING))
        # self._dbRes: None | Sequence[Row] = None
        # self._data_loader: DataLoader = DataLoader()
        # self._data_processor = None
        # self._runs: list[nx.DiGraph] = []

    # def initialize_data_processor(self):
    #     if self._data_processor == None:
    #         self._data_processor = DataProcessor(self._data_loader._data_set)

    def create_graph(self, nodes: list[WorkflowNode], edges: list[WorkflowEdge]):
        G = nx.DiGraph()
        for node in nodes:
            G.add_node(node.id, type=node.type, node_params = node.data.get("node_params") if node.data else None, category=node.data.get("category") if node.data else None)
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
            incoming_nodes = list(network.predecessors(node_id))

            print('-----incoming nodes-----', incoming_nodes)
            
            if node_category == NodeCategory.DATALOADER_DATA_LOAD_SKLEARN:
                network.nodes[node_id]['exec-result'] = DataLoader.load_sklearn_sample_dateset()
            elif node_category == NodeCategory.DATALOADER_SHOW_DATA_INFO:
                data_set: DataSet = network.nodes[incoming_nodes[0]]['exec-result']
                print(DataLoader.show_dataframe_info(data_set.data))
            elif node_category == NodeCategory.SQL_GET_DB_INSTANCE:
                network.nodes[node_id]['exec-result'] = RDB.get_instance(str(CONNECTION_STRING))
            elif node_category == NodeCategory.SQL_Select_on_Table:
                engine = network.nodes[incoming_nodes[0]]['exec-result']
                # engine = RDB.get_instance(str(CONNECTION_STRING))

                table_name = network.nodes[node_id]['data'].get("table_name")
                columns = network.nodes[node_id]['data'].get("columns", [])
                metadata = network.nodes[node_id]['data'].get("metadata")

                if table_name and metadata:
                    query = RDB.select(table_name, *columns, engine=engine, metadata=metadata)
                    network.nodes[node_id]['exec-result'] = query
            elif node_category == NodeCategory.DATALOADER_DATA_LOAD_CSV:
                network.nodes[node_id]['exec-result'] = DataLoader.read_csv()


        # print('-------Run Info-------\n', nx.get_node_attributes(network, 'exec-result'))
            