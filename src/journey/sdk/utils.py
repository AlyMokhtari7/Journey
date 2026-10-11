from typing import Protocol


class NodeUtils(Protocol):

    # def get_ancesstor_nodes(self):
    #     pass

    def log(self, log_msg, node_name) -> None:
        pass

    def set_error(self, err_msg, node_name) -> None:
        pass
