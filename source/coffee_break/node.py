from abc import ABC, abstractmethod
from pathlib import Path


class Node(ABC):
    def __init__(self):
        self._producer_task = None

    @property
    def cache_id(self) -> str:
        return self._cache_id()

    @property
    def cache_value(self) -> any:
        return self._cache_value()

    @abstractmethod
    def _cache_id(self) -> any:
        pass

    @abstractmethod
    def _cache_value(self) -> any:
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

    def _cache_id(self):
        return str(self.value)

    def _cache_value(self):
        return self.value

    def __repr__(self):
        return f"Value({self.value!r})"


class File(Node):
    def __init__(self, path: Path | str):
        super().__init__()
        self.path = Path(path)

    def _cache_id(self) -> str:
        return str(self.path)

    def _cache_value(self) -> float:
        try:
            return self.path.stat().st_mtime
        except FileNotFoundError:
            return None

    def __repr__(self):
        return f"File({self.path!r})"

