import os
import builtins
from json import dumps
from logger.logger import Logger
from client.client import RestClient

builtins._log = Logger().get_logger()


def pytest_sessionstart(session):
    """
    Before hook
    """
    create_pet()
    return session


def pytest_sessionfinish(session, exitstatus):
    """
    After hook for pytest session
    :param session: session
    :param exitstatus: exitstatus
    :return:
    """

    return session, exitstatus


def create_pet():
    client = RestClient()
    test_data1 = dumps(
        {
            "id": 1,
            "category": {"id": 0, "name": "pajaro"},
            "name": "pupo",
            "photoUrls": ["string"],
            "tags": [{"id": 0, "name": "string"}],
            "status": "available",
        }
    )
    test_data2 = dumps(
        {
            "id": 1,
            "category": {"id": 0, "name": "Pomeranian"},
            "name": "kurikuri",
            "photoUrls": ["string"],
            "tags": [{"id": 0, "name": "string"}],
            "status": "available",
        }
    )
    client.access_endpoint(method="POST", endpoint="pet", request_body=test_data1)
    client.access_endpoint(method="POST", endpoint="pet", request_body=test_data2)
