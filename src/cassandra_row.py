from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(init=False)
class CassandraRowWrapper:
    chat_id: str
    msg_id: int
    msg_link: str
    msg_date: datetime
    msg_time: datetime
    msg_author_id: int
    msg_author_first_name: str
    msg_author_last_name: str
    msg_author_username: str
    msg_text: str

    def __init__(self, row: Any):
        self.chat_id = row.chat_id
        self.msg_id = row.msg_id
        self.msg_link = row.msg_link
        self.msg_date = row.msg_date
        self.msg_time = row.msg_time
        self.msg_author_id = row.msg_author_id
        self.msg_author_first_name = row.msg_author_first_name
        self.msg_author_last_name = row.msg_author_last_name
        self.msg_author_username = row.msg_author_username
        self.msg_text = row.msg_text
