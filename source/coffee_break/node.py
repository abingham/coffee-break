from abc import abstractmethod
from pathlib import Path


class Node:
    def __init__(self):
        self._producer_task = None

    @abstractmethod
    def cache_value(self) -> any:
        pass

    @property
    def producer_task(self):
        return self._producer_task

    @producer_task.setter
    def producer_task(self, task):
        if task is None:
            raise ValueError("Cannot set producer task to None")

        if self._producer_task is not None:
            raise ValueError(f"{self!r} already has a producer task")

        self._producer_task = task


class Value(Node):
    def __init__(self, value: any):
        super().__init__()
        self.value = value

    def cache_value(self):
        return self.value

    def __repr__(self):
        return f"Value({self.value!r})"


class File(Node):
    def __init__(self, path: Path | str):
        super().__init__()
        self.path = Path(path)

    def cache_value(self) -> float:
        try:
            return self.path.stat().st_mtime
        except FileNotFoundError:
            return None

    def __repr__(self):
        return f"File({self.path!r})"

