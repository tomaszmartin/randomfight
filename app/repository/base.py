"""Base class for Data Repository sublclassess"""
import abc
from typing import Dict, Optional


class AbstractRepository(abc.ABC):
    """Abstract class for handling persistance of data."""

    def get(self, identifier: str) -> Optional[Dict]:
        """This method returns an object with a specified ID.

        Args:
            identifier: object identifier.

        Returns:
            instance of the object if available.
        """
        return self._get(identifier)

    @abc.abstractmethod
    def _get(self, identifier: str) -> Optional[Dict]:
        raise NotImplementedError

    def add(self, data: Dict) -> None:
        """Inserts object into the repository. This will not persist
        the object, only store it temporarly. For persistance call
        commit.

        Args:
            data: data to be stored.
        """
        self._add(data)

    @abc.abstractmethod
    def _add(self, data: Dict) -> None:
        raise NotImplementedError


class DataRepositoryError(Exception):
    """Indicates error in data repository."""


class DataIntegrityError(DataRepositoryError):
    """Indicates data integrity error,
    like duplicated primary key, etc."""
