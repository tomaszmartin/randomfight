import abc
from typing import Any, List


class DataRepository(abc.ABC):
    """Abstract class for handling persistance of data."""

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
    def present(self, id: List[str]) -> List[str]:
        """This method takes a list of identifiers
        and returns a subset of that lists with identifiers
        that are present in the repository.

        Args:
            id (List[str]): list of identifiers.

        Returns:
            List[bool]: list of found identifiers.
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