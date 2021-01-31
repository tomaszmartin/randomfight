"""Data Repository for data persistance."""
import abc
from typing import Dict, Optional
import os

import pandas as pd


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
        the object, only store it temporarly in memory.
        For persistance call commit.

        Args:
            data: data to be stored.
        """
        self._add(data)

    @abc.abstractmethod
    def _add(self, data: Dict) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        """Persists data from memory to drive.
        Similar in effect to SQL commit, or
        saving file to a disk.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _commit(self) -> None:
        raise NotImplementedError


class DataRepositoryError(Exception):
    """Indicates error in data repository."""


class DataIntegrityError(DataRepositoryError):
    """Indicates data integrity error,
    like duplicated primary key, etc."""


class CSVRepository(AbstractRepository):
    """Persists data in a CSV file."""

    def __init__(self, path: str, id_column: str) -> None:
        """Initalizes data respository as a .csv file.

        Args:
            path: path to the file.
            id_column: column name where object id is stored.
        """
        self.path = path
        self.id_column = id_column
        if os.path.exists(self.path):
            self.data = pd.read_csv(self.path)
        else:
            self.data = pd.DataFrame()

    def _get(self, identifier: str) -> Optional[Dict]:
        subset = self.data.loc[self.data[self.id_column] == identifier]
        results = subset.to_dict("records")
        if len(results) == 1:
            return results[0]
        if len(results) > 1:
            msg = f"Duplicate entries for id: {identifier}"
            raise DataIntegrityError(msg)
        return None

    def _add(self, data: Dict) -> None:
        current_id = data[self.id_column]
        if self.get(current_id):
            msg = f"Instance with id: {current_id} already in repository!"
            raise DataIntegrityError(msg)
        self.data = self.data.append(data, ignore_index=True)

    def _commit(self):
        self.data.to_csv(self.path)
