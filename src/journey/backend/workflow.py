import os

import networkx as nx
import sqlalchemy as sa
from dotenv import load_dotenv

from journey.backend.intermediate_artifacts import (
    DataSet,
    NodeCategory,
    WorkflowEdge,
    WorkflowNode,
)
from journey.backend.RDB import RDB
from journey.sdk.base import NodeModel
from journey.sdk.utils import NodeUtils
from modules.CoreModules import ShowDataFrameInfo
from modules.csv import ReadCSV
from modules.database import SelectData
from modules.sklearn import SklearnDataSets

# --- Env Data ---
load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
CSV_FILE_LOCATION = os.getenv("CSV_FILE_LOCATION")


class WorkflowUtils(NodeUtils):
    def log(self, log_msg, node_name) -> None:
        print(f"LOG/{node_name}/{log_msg}")

    def set_error(self, err_msg, node_name) -> None:
        print(f"ERR/{node_name}/{err_msg}")


class Workflow:
    def __init__(self) -> None:
        self._name: str = "New Workflow"
        self._network = nx.DiGraph()
        self.utils = WorkflowUtils()

        self._node_registry: dict[str, type[NodeModel]] = {
            "read_csv": ReadCSV,
            "select_on_DB": SelectData,
            "show_dataFrame_info": ShowDataFrameInfo,
            "load_sklearn_sample_dateset": SklearnDataSets,
        }

        self._nodes_instance_cache: dict[str, NodeModel] = {}

    def _get_node_instance(self, node_name: str) -> NodeModel:
        if node_name not in self._nodes_instance_cache:
            print(
                "-" * 10,
                f" Initializing new instance of {node_name} ",
                "-" * 10,
                end="\n",
            )
            node_instance = self._node_registry[node_name]()
            self._nodes_instance_cache[node_name] = node_instance  # Instantiate ONCE

        return self._nodes_instance_cache[node_name]

    def create_graph(self, nodes: list[WorkflowNode], edges: list[WorkflowEdge]):
        G = nx.DiGraph()
        for node in nodes:
            G.add_node(
                node.id,
                type=node.type,
                data=node.data,
                category=node.data.get("category") if node.data else None,
            )
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

        print("---------Execution----------")
        for node_id in order:
            node_category = network.nodes[node_id]["category"]
            incoming_nodes = list(network.predecessors(node_id))

            print("-----incoming nodes-----", incoming_nodes)

            if node_category == NodeCategory.DATALOADER_DATA_LOAD_SKLEARN:
                network.nodes[node_id]["exec-result"] = (
                    self._get_node_instance('load_sklearn_sample_dateset').execute(context={}, utils=self.utils)
                )
            elif node_category == NodeCategory.DATALOADER_SHOW_DATA_INFO:
                data_frame: DataSet = network.nodes[incoming_nodes[0]]["exec-result"]
                context = {"data_frame": data_frame}
                network.nodes[node_id]["exec-result"] = self._get_node_instance('show_dataFrame_info').execute(context=context, utils=self.utils)
            elif node_category == NodeCategory.SQL_SELECT_ON_TABLE:
                # engine = network.nodes[incoming_nodes[0]]['exec-result']
                engine = RDB.get_instance(str(CONNECTION_STRING))

                table_name = network.nodes[node_id]["data"].get("tableName")
                columns = network.nodes[node_id]["data"].get("columns", [])
                metadata = sa.MetaData()

                context = {
                    "sa_engine": engine,
                    "sa_metadata": metadata,
                    "table_name": table_name,
                    "columns": columns,
                }
                network.nodes[node_id]["exec-result"] = self._get_node_instance(
                    "select_on_DB"
                ).execute(context=context, utils=self.utils)
            elif node_category == NodeCategory.DATALOADER_DATA_LOAD_CSV:
                context = {"file_name": CSV_FILE_LOCATION}
                network.nodes[node_id]["exec-result"] = self._get_node_instance(
                    "read_csv"
                ).execute(context=context, utils=self.utils)

        # print('-------Run Info-------\n', nx.get_node_attributes(network, 'exec-result'))
