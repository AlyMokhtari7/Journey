from abc import ABC, abstractmethod
from typing import Any

from journey.sdk.utils import NodeUtils


class NodeModel(ABC):

    @abstractmethod
    def execute(self, context: dict[str, Any], utils: NodeUtils) -> Any:
        pass
