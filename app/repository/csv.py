"""CSV based Repository"""
from typing import Dict, Optional

import pandas as pd

from app.repository import base


class CSVRepository(base.AbstractRepository):
    """Persists data in a CSV file."""

    def __init__(self, path: str, id_column: str) -> None:
        """Initalizes data respository as a .csv file.

        Args:
            path: path to the file.
            id_column: column name where object id is stored.
        """
        self.path = path
        self.id_column = id_column
        self.data = pd.read_csv(self.path)

    def _get(self, identifier: str) -> Optional[Dict]:
        subset = self.data.loc[self.data[self.id_column] == identifier]
        results = subset.to_dict("records")
        if len(results) == 1:
            return results[0]
        if len(results) > 1:
            msg = f"Duplicate entries for {identifier}"
            raise base.DataIntegrityError(msg)
        return None

    def _add(self, data: Dict) -> None:
        current_id = data[self.id_column]
        if self.get(current_id):
            msg = f"Instance with {current_id} already in repository!"
            raise base.DataIntegrityError(msg)
        self.data = self.data.append(data, ignore_index=True)
