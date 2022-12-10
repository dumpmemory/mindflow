"""
This module contains the logic for generating the prompt for the chatbot.
"""
import json
import subprocess

from mindflow.resolve.resolve import resolve
from mindflow.utils.prompts import GIT_DIFF_PROMPT_PREFIX

from mindflow.query.mfq import MindFlowQueryHandler, MFQ_FILE


def generate_diff_prompt(args):
    """
    This function is used to generate a prompt for the chatbot based on the git diff.
    """
    command = ["git", "diff"] + args.diffargs

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")

    return f"{GIT_DIFF_PROMPT_PREFIX}\n\n{diff_result}"


def generate_prompt_from_files(args, model, user_query: str):
    """
    This function is used to generate a prompt based on a question or summarization task
    """
    reference_text_dict = {}

    refs = set(args.references)

    if MFQ_FILE in refs:
        # When an MFQ_FILE is passed, this is a special case of the query command.
        q = MindFlowQueryHandler(user_query, refs)
        prompt = q.get_prompt()
    else:
        {reference_text_dict.update(resolve(reference, model, user_query)) for reference in refs}
        context_prompt = json.dumps(reference_text_dict, indent=4)
        prompt = f"{user_query}\n\n{context_prompt}"

    return prompt
