from typing import List
from .node import Node


class Task:
    def __init__(self, input_nodes, output_nodes):
        self.input_nodes: List[Node] = list(input_nodes)
        self.output_nodes: List[Node] = list(output_nodes)

        for output_node in output_nodes:
            output_node.producer_task = self

    def __repr__(self):
        return f"Task(input_nodes={self.input_nodes!r}, output_nodes={self.output_nodes!r})"
