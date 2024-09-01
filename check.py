import os
import sys
# import logging
#
# logging.basicConfig(level=logging.DEBUG)

#
# # Get the parent directory of the current file
# target_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "databricks-sql-python", "src"))
#
# # Add the parent directory to sys.path
# sys.path.append(target_folder_path)

from databricks import sql

# from dotenv import load_dotenv

#  export DATABRICKS_TOKEN=whatever


# Load environment variables from .env file
# load_dotenv()

host = os.getenv("MY_SERVER_HOSTNAME")
http_path = os.getenv("MY_HTTP_PATH")
access_token = os.getenv("MY_TOKEN")

connection = sql.connect(
    server_hostname=host,
    http_path=http_path,
    access_token=access_token)


cursor = connection.cursor()
cursor.execute("select * from `auto_maintenance_bugbash`.`tpcds_sf1000_naga_testv32`.`store_sales` LIMIT 1000")
# cursor.execute('SELECT 1')
result = cursor.fetchmany(10)
for row in result:
    print(row)

cursor.close()
connection.close()