import os
from dotenv import load_dotenv
load_dotenv()
from databricks import sql

HOSTNAME = os.getenv("DATABRICKS_HOSTNAME")
HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
TOKEN = os.getenv("DATABRICKS_TOKEN")

def get_connection():
    return sql.connect(
        server_hostname=HOSTNAME,
        http_path=HTTP_PATH,
        access_token=TOKEN
    )

def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM retailanalytics.masterdata.productmaster
        WHERE isactive = TRUE
    """)

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return products

def get_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM retailanalytics.masterdata.customermaster
        WHERE isactive = TRUE
    """)

    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return customers

def get_stores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM retailanalytics.masterdata.storemaster
        WHERE isactive = TRUE
    """)

    stores = cursor.fetchall()

    cursor.close()
    conn.close()

    return stores

# products = get_products()
# customers = get_customers()
# stores = get_stores()

# print(f"Products  : {len(products)}")
# print(f"Customers : {len(customers)}")
# print(f"Stores    : {len(stores)}")