import os
import pytest


@pytest.fixture(scope="session")
def benchmarking_host():
    return os.getenv("BENCHMARKING_SERVER_HOSTNAME")


@pytest.fixture(scope="session")
def benchmarking_http_path():
    return os.getenv("BENCHMARKING_HTTP_PATH")


@pytest.fixture(scope="session")
def benchmarking_access_token():
    return os.getenv("BENCHMARKING_TOKEN")


@pytest.fixture(scope="session")
def benchfood_host():
    return os.getenv("BENCHFOOD_SERVER_HOSTNAME")


@pytest.fixture(scope="session")
def benchfood_http_path():
    return os.getenv("BENCHFOOD_HTTP_PATH")


@pytest.fixture(scope="session")
def benchfood_access_token():
    return os.getenv("BENCHFOOD_TOKEN")


@pytest.fixture(scope="session", autouse=True)
def connection_details(benchmarking_host, benchmarking_http_path, benchmarking_access_token, benchfood_host, benchfood_http_path, benchfood_access_token):
    return {
        "benchmarking_host": benchmarking_host,
        "benchmarking_http_path": benchmarking_http_path,
        "benchmarking_access_token": benchmarking_access_token,
        "benchfood_host": benchfood_host,
        "benchfood_http_path": benchfood_http_path,
        "benchfood_access_token": benchfood_access_token,
    }
