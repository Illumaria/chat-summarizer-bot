from typing import Any, List

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session
from telegram import Message

from src.cassandra_row import CassandraRowWrapper
from src.constants import (
    ASTRA_DB_KEYSPACE,
    ASTRA_DB_PASSWORD,
    ASTRA_DB_SCB_PATH,
    ASTRA_DB_TABLE_NAME,
    ASTRA_DB_USERNAME,
)


def create_session() -> Session:
    """
    Establish a connection with AstraDB cluster
    :return: Session, a session instance
    """
    cloud_config = {
        "secure_connect_bundle": ASTRA_DB_SCB_PATH,
        "use_default_tempdir": True,
    }
    auth_provider = PlainTextAuthProvider(
        username=ASTRA_DB_USERNAME,
        password=ASTRA_DB_PASSWORD,
    )
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect(ASTRA_DB_KEYSPACE)
    return session


def create_table(session: Session) -> None:
    session.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {ASTRA_DB_KEYSPACE}.{ASTRA_DB_TABLE_NAME} (
                chat_id text,
                msg_id int,
                msg_link text,
                msg_date date,
                msg_time time,
                msg_author_id int,
                msg_author_first_name text,
                msg_author_last_name text,
                msg_author_username text,
                msg_text text,
                PRIMARY KEY ((chat_id, msg_date), msg_id)
            );
            """
    )


def set_message(session: Session, message: Message) -> None:
    chat_id = str(message.chat_id)
    msg_id = message.message_id
    msg_link = message.link or "no_link"
    msg_date = message.date.date().isoformat()
    msg_time = message.date.time().isoformat()
    msg_author_id = message.from_user.id
    msg_author_first_name = message.from_user.first_name
    msg_author_last_name = message.from_user.last_name
    msg_author_username = message.from_user.username
    msg_text = message.text

    session.execute(
        f"INSERT INTO {ASTRA_DB_TABLE_NAME} "
        "(chat_id, msg_id, msg_link, msg_date, msg_time, "
        "msg_author_id, msg_author_first_name, "
        "msg_author_last_name, msg_author_username, msg_text) VALUES ("
        f"'{chat_id}',{msg_id},'{msg_link}','{msg_date}','{msg_time}',{msg_author_id},"
        f"'{msg_author_first_name}','{msg_author_last_name}','{msg_author_username}',"
        f"'{msg_text}')"
    )


def get_messages(session: Session, chat_id: str, msg_date: str) -> List[Any]:
    result = session.execute(
        f"SELECT * FROM {ASTRA_DB_TABLE_NAME} "
        f"WHERE chat_id = '{chat_id}' AND msg_date = '{msg_date}'"
    ).all()
    history = [CassandraRowWrapper(row) for row in result]
    return history


def update_message(session: Session, edited_message: Message) -> None:
    prepared = session.prepare(
        f"UPDATE {ASTRA_DB_TABLE_NAME} SET msg_text = ? "
        "WHERE chat_id = ? AND msg_date = ? AND msg_id = ?"
    )

    chat_id = str(edited_message.chat_id)
    msg_id = edited_message.message_id
    msg_date = edited_message.date.date().isoformat()
    new_msg_text = edited_message.text

    session.execute(prepared, [new_msg_text, chat_id, msg_date, msg_id])


def delete_messages(session: Session, chat_id: str, msg_date: str) -> None:
    prepared = session.prepare(
        f"DELETE FROM {ASTRA_DB_TABLE_NAME} " "WHERE chat_id = ? AND msg_date = ?"
    )
    session.execute(prepared, [chat_id, msg_date])
