import logging
import sqlite3
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)


def no_ctx_manager() -> None:
    """Connect to a database without a context manager"""
    logging.basicConfig(level=logging.INFO)
    conn = sqlite3.connect(":memory:")
    try:
        curr = conn.cursor()

        curr.execute("CREATE TABLE blogs (name text, url text)")
        curr.execute(
            "INSERT INTO blogs (name, url) VALUES ('The Python Standard Library', 'https://docs.python.org/3/')"
        )
        curr.execute("SELECT * FROM blogs")

        logging.info(curr.fetchall())
    finally:
        conn.close()  # Manually close the connection


class SQLite(object):
    """Context manager Class to manage a sqlite3 database connection"""

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)

    def __enter__(self) -> sqlite3.Cursor:
        logging.info("Calling __enter__")
        return self.connection.cursor()

    def __exit__(self, *_) -> None:
        logging.info("Calling __exit__")
        self.connection.commit()
        self.connection.close()


def ctx_manager_class() -> None:
    """Using a custom class to manage a database connection"""

    # with statement calls __enter__ and __exit__ automatically
    with SQLite(":memory:") as curr:
        curr.execute("CREATE TABLE blogs (name text, url text)")
        curr.execute(
            "INSERT INTO blogs (name, url) VALUES ('The Python Standard Library', 'https://docs.python.org/3/')"
        )
        curr.execute("SELECT * FROM blogs")

        logging.info(curr.fetchall())


@contextmanager
def open_database(file_name: str) -> sqlite3.Cursor:
    """Context manager function to manage a database connection"""
    connection = sqlite3.connect(file_name)
    try:
        cursor = connection.cursor()
        yield cursor  # use yield to continue execution
    except sqlite3.DatabaseError as err:
        logging.error(err)
    finally:
        logging.info("Closing connection")
        connection.commit()
        connection.close()


def ctx_manager_decorator() -> None:
    """Using a decorated function to manage a database connection"""
    with open_database(":memory:") as curr:  # This is simpler, but the types get messy
        curr.execute("CREATE TABLE blogs (name text, url text)")
        curr.execute(
            "INSERT INTO blogs (name, url) VALUES ('The Python Standard Library', 'https://docs.python.org/3/')"
        )
        curr.execute("SELECT * FROM blogs")

        logging.info(curr.fetchall())


if __name__ == "__main__":
    # no_ctx_manager()
    # ctx_manager_class()
    ctx_manager_decorator()
