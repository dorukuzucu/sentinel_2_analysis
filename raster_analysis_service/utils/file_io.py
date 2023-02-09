import glob
from itertools import chain
from typing import Iterator, List


class Globber:
    """A class to create glob based on one or multiple extensions
    """
    _extensions: List[str]
    _starting_directory: str

    def __init__(self, starting_directory) -> None:
        self._starting_directory = starting_directory
        self._extensions = []

    def add_extension(self, extension: str):
        """Add given extension to glob list

        Args:
            extension (str): file extension to be searched
        """
        if extension.startswith("."):
            extension = extension[1:]
        if not extension in self._extensions:
            self._extensions.append(extension)

    def create(self, recursive: bool = True) -> Iterator:
        """Creates chain of iterators for globbing

        Args:
            recursive (bool, optional): If True, subdirectories will be included in search. 
                Defaults to True.

        Returns:
            Iterator: A glob iterator with files found
        """
        globbers: List[Iterator] = []
        for extension in self._extensions:
            glob_iterator = self._create_for_extension(extension, recursive)
            globbers.append(glob_iterator)
        return chain(globbers)

    def _create_for_extension(self, extension: str, recursive: bool):
        """Creates a single iterator for a single file type

        Args:
            extension (str): extension to create generator for
            recursive (bool, optional): If True, subdirectories will be included in search

        Returns:
            Iterator: A glob iterator for given extension with files found
        """
        search_string = self._build_search_string(extension, recursive)
        return glob.iglob(search_string, recursive=recursive)

    def _build_search_string(self, extension: str, recursive: bool) -> str:
        """Build and returns a search string for given extension 
        """
        search_string = self._starting_directory
        if recursive:
            search_string = search_string + "/**"
        search_string += f"/*.{extension}"
        return search_string
