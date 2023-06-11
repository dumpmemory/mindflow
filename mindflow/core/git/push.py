from typing import Tuple

from mindflow.utils.execute import execute_no_trace


def run_push(args: Tuple[str]):
    print(execute_no_trace(["git", "push"] + list(args)))
