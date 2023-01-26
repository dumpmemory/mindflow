"""
`delete` command
"""

import sys
import argparse

from typing import List
from mindflow.index.model import index, DocumentReference
from mindflow.index.resolve import resolve

from mindflow.utils.args import (
    _add_document_args,
    _add_remote_args,
)


class Delete:
    """
    Class for initializing Delete args and executing the delete command.
    """

    document_paths: List[str]
    remote: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Delete your MindFlow index.",
        )
        _add_document_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.document_paths = args.document_paths
        self.remote = args.remote

    def execute(self):
        """
        This function is used to delete your MindFlow index.
        """
        if self.remote:
            print("Remote delete not implemented yet.")
            return

        if self.document_paths == ["^"]:
            index.delete_documents()
            return

        # Resolve documents (Path, URL, etc.) and get their hashes

        document_references: List[DocumentReference] = []
        for document_path in self.document_paths:
            document_references.extend(resolve(document_path))

        index.delete_documents(document_references)
