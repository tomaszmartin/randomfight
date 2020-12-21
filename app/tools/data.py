import abc
from typing import Any


class DataRepository(abc.ABC):
    @abc.abstractmethod
    def select(self, id: str) -> Any:
        """This method returns an object with a specified ID.

        Args:
            id (str): object identifier.

        Returns:
            Any: instance of the object.
        """
        pass

    @abc.abstractmethod
    def insert(self, instance: Any) -> bool:
        """Inserts object into the repository. This will not persist
        the object, only store it temporarly. For persistance call
        commit.

        Args:
            instance (Any): object to be stored.

        Returns:
            bool: whether operation was successful.
        """
        pass

    @abc.abstractmethod
    def commit(self) -> bool:
        """Commits the changes from memory to persistent storage.

        Returns:
            bool: whether operation was successful.
        """
        pass