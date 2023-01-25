"""
Module for recursively extracting all files from a file path.
"""

import logging
import os

from typing import List

from mindflow.utils.files.git import is_within_git_repo, get_git_files


def extract_files(path: os.PathLike) -> List[os.PathLike]:
    """
    Extract all files from a directory.
    """
    file_paths = []
    if os.path.isfile(path):
        return [os.fspath(path)]
    if is_within_git_repo(path):
        return get_git_files(path)
    try:
        with os.scandir(path) as paths:
            for scanned_path in paths:
                if scanned_path.is_file():
                    file_paths.append(os.fspath(scanned_path.path))
                elif path.is_dir():
                    file_paths.extend(extract_files(scanned_path.path))
        return file_paths
    except IsADirectoryError as error:
        logging.debug("Could not read directory/file: %s", path)
        logging.debug(error)
        return file_paths
