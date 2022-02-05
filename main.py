import logging
import sqlite3
import contextlib

logging.basicConfig(level=logging.INFO)


def no_ctx_manager() -> None:
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
        conn.close()


class SQLite(object):
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
    with SQLite(":memory:") as curr:
        curr.execute("CREATE TABLE blogs (name text, url text)")
        curr.execute(
            "INSERT INTO blogs (name, url) VALUES ('The Python Standard Library', 'https://docs.python.org/3/')"
        )
        curr.execute("SELECT * FROM blogs")

        logging.info(curr.fetchall())


def ctx_manager_decorator() -> None:
    ...

if __name__ == "__main__":
    # no_ctx_manager()
    ctx_manager_class()
