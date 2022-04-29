import json
from utils.singleton import Singleton
from .constants import DataType
from pydantic import BaseModel, ValidationError
from typing import Any, Union
from logger import info, debug, error
from dataclasses import dataclass
import os

class JSONMetadata(BaseModel):
    """A pydantic model for the JSON metadata provided."""

    name: str
    description: str
    version: str
    data_type: DataType

@dataclass
class JSONDocument:
    """Dataclass containing data from a Kisumi resource formatted JSON document."""

    metadata: JSONMetadata
    data: Union[DataType, dict[str, Any]]

class JSONLoader(Singleton):
    """Class managing a repository of all Kisumi formatted JSON documents."""

    # Special methods
    def __init__(self) -> None:
        """Initialises an empty JSON loader repositository."""

        self._repo: dict[DataType, list[JSONDocument]] = {}
    
    def __len__(self) -> int:
        """Returns the number of documents stored in the repository."""

        return len(self._repo)
    
    # Public methods
    async def load(self) -> None:
        """Loads all documents inside of the `resources/json` directory and
        its subdirectories."""

        files = _crawl_json_documents()
        file_count = len(files)
        successes = 0
        info(f"Attempting to load {file_count} into the JSON repository...")

        for file in files:
            if self.load_document(file):
                debug(f"Successfully loaded {file} into the repository.")
                successes += 1
            else:
                # TODO: Specify what error happened.
                error(f"Failed loading {file} into the repository.")

        info(f"Successfully loaded {successes}/{file_count} into the JSON repository!")        
    
    def load_document(self, path: str) -> bool:
        """Loads and inserts a document from a specific path.
        
        Returns:
            `bool` relating to the success of the action.
        """

        if not os.path.exists(path):
            return False
        
        with open(path, "r") as f:
            data_json = json.load(f)
            return self.__parse_json(data_json)

    def clear(self) -> None:
        """Removes all of the items in the repository."""

        self._repo.clear()

    # Private methods.
    def __parse_json(self, d: dict[str, Any]) -> bool:
        """Attempts to parse a documents JSON into objects, inserting into the
        repo on success.
        
        Returns:
            `bool` relating to the success of the action.
        """

        try:
            metadata = JSONMetadata(**d["metadata"])
            self._repo[metadata.data_type] = JSONDocument(
                metadata= metadata,
                data= d["data"],
            )
            return True
        except (ValidationError, KeyError):
            return False

# https://stackoverflow.com/a/59596244
def _crawl_json_documents() -> list[str]:
    """Crawls the directories of all JSON documents inside of `resources/json`
    and its subdirectories."""

    return [
        os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk('.')
        for filename in filenames if filename.endswith('.json')
    ]
