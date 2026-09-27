from databricks import sql
import os

print("Testing Databricks connection...")

conn = sql.connect(
    server_hostname=os.getenv("DATABRICKS_HOSTNAME"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_TOKEN")
)

cursor = conn.cursor()

cursor.execute("SELECT current_timestamp()")

result = cursor.fetchall()

print("SUCCESS")
print(result)

cursor.close()
conn.close()
