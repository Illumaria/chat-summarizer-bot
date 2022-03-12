import logging
from typing import Any, List


def setup_logging() -> None:
    """Set logging format for the project"""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


def merge_same_author_messages(messages: List[Any], separator: str = " ") -> List[Any]:
    """
    Merge consequent messages from the same author
    :param messages: list, list of Cassandra Row objects containing message info
    :param separator: str, separator character to insert between message texts
    :return: list, list of Cassandra Row objects with merged message texts
    """
    if not messages:
        return []

    merged_messages = [messages[0]]
    for message in messages[1:]:
        if message.msg_author_id == merged_messages[-1].msg_author_id:
            merged_messages[-1].msg_text += f"{separator}{message.msg_text}"
        else:
            merged_messages.append(message)
    return merged_messages
