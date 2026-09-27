import os
from dotenv import load_dotenv
from databricks import sql

load_dotenv()

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
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM retailanalytics.masterdata.productmaster
            WHERE isactive = TRUE
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_customers():
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM retailanalytics.masterdata.customermaster
            WHERE isactive = TRUE
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_stores():
    conn = get_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM retailanalytics.masterdata.storemaster
            WHERE isactive = TRUE
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Testing Databricks Connection...")

    products = get_products()
    customers = get_customers()
    stores = get_stores()

    print(f"Products  : {len(products)}")
    print(f"Customers : {len(customers)}")
    print(f"Stores    : {len(stores)}")
