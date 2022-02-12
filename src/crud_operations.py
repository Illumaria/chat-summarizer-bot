from typing import List

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session
from telegram import Message

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
    cloud_config = {"secure_connect_bundle": ASTRA_DB_SCB_PATH}
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
                chat_id text PRIMARY KEY,
                msg_id int,
                msg_link text,
                msg_time text,
                msg_author_id int,
                msg_author_first_name text,
                msg_author_last_name text,
                msg_author_username text,
                msg_text text
            );
            """
    )


def set_message(session: Session, message: Message) -> None:
    chat_id = str(message.chat_id)
    msg_id = message.message_id
    msg_link = message.link or "no_link"
    msg_time = message.date.strftime("%T")
    msg_author_id = message.from_user.id
    msg_author_first_name = message.from_user.first_name
    msg_author_last_name = message.from_user.last_name
    msg_author_username = message.from_user.username
    msg_text = message.text

    session.execute(
        f"INSERT INTO {ASTRA_DB_TABLE_NAME} "
        "(chat_id, msg_id, msg_link, msg_time, msg_author_id, msg_author_first_name, "
        "msg_author_last_name, msg_author_username, msg_text) VALUES ("
        f"'{chat_id}',{msg_id},'{msg_link}','{msg_time}',{msg_author_id},"
        f"'{msg_author_first_name}', '{msg_author_last_name}','{msg_author_username}',"
        f"'{msg_text}')"
    )


def get_messages(session: Session, primary_key: str) -> List[str]:
    # TODO: deal with primary key
    result = session.execute(
        f"SELECT * FROM {ASTRA_DB_TABLE_NAME} " f"WHERE primary_key = {primary_key}"
    )
    return result


def update_message(session: Session, edited_message: Message) -> None:
    # TODO: deal with primary key
    prepared = session.prepare(
        f"UPDATE {ASTRA_DB_TABLE_NAME} SET msg_text = ? WHERE primary_key = ?"
    )

    chat_id = str(edited_message.chat_id)
    msg_id = edited_message.message_id
    new_msg_text = edited_message.text

    session.execute(prepared, [new_msg_text, chat_id, msg_id])


def delete_messages(session: Session, primary_key: str) -> None:
    # TODO: deal with primary key
    prepared = session.prepare(
        f"DELETE FROM {ASTRA_DB_TABLE_NAME} WHERE primary_key = ?"
    )
    session.execute(prepared, [primary_key])
