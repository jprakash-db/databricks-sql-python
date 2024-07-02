import pandas as pd
import databricks.sql as sql
import os
# import databricks.sqlalchemy as sqlalchemy

server_hostname = os.getenv("DATABRICKS_HOST")
http_path = os.getenv("DATABRICKS_HTTP_PATH")

access_token = os.getenv("DATABRICKS_TOKEN")

extra_connect_args = {
    "_tls_verify_hostname": True,
    "_user_agent_entry": "PySQL Example Script",
}

# with sql.connect(
#     server_hostname=server_hostname,
#     http_path=http_path,
#     access_token=access_token,
#     use_cloud_fetch=True,
# ) as conn:
#     print("Connected to Databricks SQL endpoint.")
#     with conn.cursor() as cursor:
#         cursor.execute("select * from hive_metastore.hive_metastore.customers_csv LIMIT 10")
#         rows = cursor.fetchall()
#         print(pd.DataFrame(rows))

from databricks.sqlalchemy import TIMESTAMP, TINYINT
from sqlalchemy import text, create_engine


engine = create_engine(
    f"databricks://token:{access_token}@{server_hostname}?http_path={http_path}",
    connect_args=extra_connect_args, echo=True,
)
print("Engine created....")
with engine.connect() as conn:
    print(pd.read_sql("select * from hive_metastore.hive_metastore.customers_csv LIMIT 10", conn))
