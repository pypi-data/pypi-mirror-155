import gc
import sqlite3
import logging
from logging.handlers import QueueHandler
from queue import Queue
from ewokscore.logging_utils.cleanup import cleanup_logger
from ewokscore.logging_utils import handlers


def test_cleanup_logger():
    logger = logging.getLogger(__name__)
    q = Queue()
    h = QueueHandler(q)
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    h.setLevel(logging.INFO)

    logger.info("info message 1")
    assert q.qsize() == 1

    cleanup_logger(__name__)
    assert q.qsize() == 0


def test_connection_handler():
    connected = None
    destination = list()
    expected = list()

    class Connection:
        def __init__(self):
            nonlocal connected
            connected = True

        def __del__(self):
            nonlocal connected
            connected = False

    class MyHandler(handlers.ConnectionHandler):
        def _connect(self, timeout=1) -> None:
            self._connection = Connection()

        def _disconnect(self) -> None:
            del self._connection
            self._connection = None

        def _send_serialized_record(self, srecord):
            destination.append(srecord)

        def _serialize_record(self, record):
            msg = self.format(record)
            return record.levelno, msg

    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)
    handler = MyHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Check lazy connecting
    assert not connected
    assert destination == expected

    logger.debug("debug message")
    assert not connected
    assert destination == expected

    logger.info("info message 1")
    expected.append((logging.INFO, "info message 1"))
    assert connected
    assert destination == expected

    # Check closing a handler
    handler.close()
    assert not connected

    # Check reconnect
    logger.info("info message 2")
    expected.append((logging.INFO, "info message 2"))
    assert connected
    assert destination == expected

    # Check connection closed when no reference to the handler anymore
    logger.removeHandler(handler)
    handler = None
    while gc.collect():
        pass
    assert not connected

    handler = MyHandler()
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info("info message 3")
    expected.append((logging.INFO, "info message 3"))
    assert connected
    assert destination == expected

    # Check connection closed when no reference to the logger anymore
    handler = None
    logger = None
    cleanup_logger(__name__)
    while gc.collect():
        pass
    assert not connected


def test_sqlite3_handler(tmpdir):
    logger = logging.getLogger(__name__)
    uri = str(tmpdir / "test.db")
    handler = handlers.Sqlite3Handler(uri, "mytable", ["field1", "field2"])
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)

    expected = list()
    logger.info("message1")
    expected.append((None, None))
    logger.info("message2", extra={"field2": "2"})
    expected.append((None, "2"))
    logger.info("message2", extra={"field1": 1, "field2": "2"})
    expected.append(("1", "2"))

    with sqlite3.connect(uri, uri=True, check_same_thread=False) as conn:
        rows = list(conn.cursor().execute("SELECT * FROM mytable"))

    assert rows == expected

    cleanup_logger(__name__)


def test_async_wrapper():
    logger = logging.getLogger(__name__)
    q = Queue()
    h = handlers.AsyncHandlerWrapper(QueueHandler(q))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)
    h.setLevel(logging.INFO)

    logger.info("message")
    assert q.get(timeout=3).msg == "message"

    cleanup_logger(__name__)
