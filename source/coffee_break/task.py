import json
from typing import List
from .node import Node


class Task:
    def __init__(self, input_nodes, output_nodes):
        self.input_nodes: List[Node] = list(input_nodes)
        self.output_nodes: List[Node] = list(output_nodes)

        for output_node in output_nodes:
            output_node.producer_task = self

    @property
    def cache_id(self) -> str:
        type_id = f"{type(self).__module__}.{type(self).__name__}"
        input_ids = [node.cache_id for node in self.input_nodes]
        output_ids = [node.cache_id for node in self.output_nodes]
        id_struct = {
            "type": type_id,
            "inputs": input_ids,
            "outputs": output_ids,
        }
        return json.dumps(id_struct, sort_keys=True)

    @property
    def cache_value(self) -> any:
        input_values = [node.cache_value for node in self.input_nodes]
        output_values = [node.cache_value for node in self.output_nodes]
        return {
            "inputs": input_values,
            "outputs": output_values,
        }

    def __repr__(self):
        return f"Task(input_nodes={self.input_nodes!r}, output_nodes={self.output_nodes!r})"
