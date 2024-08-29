import random
import time
from databricks import sql
import logging
import pytest
from contextlib import contextmanager
from datetime import datetime
log = logging.getLogger(__name__)


class TestBenchmarkingSuite:

    # TAG = "PRE-SPLIT"
    TAG = "POST-SPLIT"
    CATALOG_NAME = "main"
    SCHEMA_NAME = "tpcds_sf100_delta"
    TABLE_NAME = "catalog_sales"
    RESULTS_TABLE = "main.pysql_benchmarking_schema.benchmarking_results"
    ATTEMPTS = 10
    ROWS = 1000000
    LARGE_QUERY_LIMIT = 1000000
    SMALL_QUERY_LIMIT = 10000

    @pytest.fixture(autouse=True)
    def get_details(self, connection_details):
        self.arguments = connection_details.copy()

        self.benchmarking_connection_params = {
            "server_hostname": self.arguments["benchmarking_host"],
            "http_path": self.arguments["benchmarking_http_path"],
            "access_token": self.arguments["benchmarking_access_token"]
        }

        self.benchfood_connection_params = {
            "server_hostname": self.arguments["benchfood_host"],
            "http_path": self.arguments["benchfood_http_path"],
            "access_token": self.arguments["benchfood_access_token"]
        }

    @contextmanager
    def connection(self, connection_params):
        log.info("Connecting with args: {}".format(connection_params))
        conn = sql.connect(**connection_params)

        try:
            yield conn
        finally:
            conn.close()

    @contextmanager
    def cursor(self, connection_params):
        with self.connection(connection_params) as conn:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                cursor.close()

    def removed_outlier_mean(self, data):
        total = 0
        for i in range(1, len(data)-1):
            total += data[i]

        return total/(len(data)-2)

    def insert_benchmarking_results_data(self, function_name, query_time):

        log.info(f"Inserting results {self.TAG} - {function_name}")
        with self.cursor(self.benchfood_connection_params) as cursor:
            cursor.execute(
                f"INSERT INTO {self.RESULTS_TABLE} (tag, function_name, compute_duration, date_time) VALUES ('{self.TAG}', '{function_name}', {query_time}, '{datetime.now()}')"
            )

    def get_query_time(self, query, expected_num_rows):
        start_time = time.time()
        with self.cursor(self.benchmarking_connection_params) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            log.info("Fetched {} rows".format(len(result)))

            assert len(result) == expected_num_rows

        end_time = time.time()
        elapsed_time = end_time - start_time

        return elapsed_time

    def test_large_queries_performance(self):
        compute_duration = []
        function_name = "large_query"

        for i in range(0, self.ATTEMPTS):
            log.info("Attempt: {}".format(i))
            offset = i * self.LARGE_QUERY_LIMIT + random.randint(1, self.LARGE_QUERY_LIMIT)

            query = "select * from {}.{}.{} LIMIT {} OFFSET {}".format(self.CATALOG_NAME, self.SCHEMA_NAME, self.TABLE_NAME, self.LARGE_QUERY_LIMIT, offset)
            compute_duration.append(self.get_query_time(query, self.LARGE_QUERY_LIMIT))

        compute_duration.sort()
        self.insert_benchmarking_results_data(function_name, self.removed_outlier_mean(compute_duration))

    def test_small_queries_performance(self):
        compute_duration = []
        function_name = "small_query"

        for i in range(0, self.ATTEMPTS):
            log.info("Attempt: {}".format(i))
            offset = i * self.SMALL_QUERY_LIMIT + random.randint(1, self.SMALL_QUERY_LIMIT)

            query = "select * from {}.{}.{} LIMIT {} OFFSET {}".format(self.CATALOG_NAME, self.SCHEMA_NAME, self.TABLE_NAME, self.SMALL_QUERY_LIMIT, offset)
            compute_duration.append(self.get_query_time(query, self.SMALL_QUERY_LIMIT))

        compute_duration.sort()
        self.insert_benchmarking_results_data(function_name, self.removed_outlier_mean(compute_duration))


