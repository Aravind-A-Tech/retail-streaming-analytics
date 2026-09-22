import random
import os
from datetime import datetime, UTC
import uuid
from kafkaproducer import send_transaction

from readdatabricks import (
    get_products,
    get_customers,
    get_stores
)


class TransactionGenerator:

    def __init__(self, products, customers, stores):
        self.products = products
        self.customers = customers
        self.stores = stores

    def generate_transaction_id(self):
        transaction_id = (f"TXN-{datetime.now(UTC).strftime('%Y%m%d')}-"f"{uuid.uuid4().hex[:8]}")
        return transaction_id

    def generate_transaction(self):

        product = random.choice(self.products)
        customer = random.choice(self.customers)
        store = random.choice(self.stores)
        quantity = random.choices(
                [1, 2, 3],
                weights=[70, 25, 5],
                k=1
            )[0]
        unit_price = float(product.unitprice)
        gross_amount = round(quantity * unit_price,2)
        payment_method = random.choice([
            "UPI",
            "Credit Card",
            "Debit Card",
            "Cash",
            "Wallet"
        ])
        transaction_status = random.choices( ["COMPLETED", "FAILED", "PENDING"],weights=[95, 3, 1],k=1)[0]

        transaction = {
            "transaction_id": self.generate_transaction_id(),
            "transaction_ts": datetime.now(UTC).isoformat(),

            "customer_id": customer.customerid,
            "product_id": product.productid,
            "store_id": store.storeid,

            "quantity": quantity,
            "unit_price": unit_price,
            "gross_amount": gross_amount,

            "payment_method": payment_method,
            "transaction_status": transaction_status
        }
        return transaction


def main():

    print("Loading master data...")

    products = get_products()
    customers = get_customers()
    stores = get_stores()

    print(f"Products  : {len(products)}")
    print(f"Customers : {len(customers)}")
    print(f"Stores    : {len(stores)}")

    generator = TransactionGenerator(
        products,
        customers,
        stores
    )

    print("\nGenerating sample transactions...\n")
   
    current_hour = datetime.now(UTC).hour
    if 6 <= current_hour < 10:
        gen_count = random.randint(40, 80)

    elif 17 <= current_hour < 22:
        gen_count = random.randint(49, 100)

    else:
        gen_count = random.randint(10, 40)

    count = int(os.getenv("TXN_COUNT") or gen_count)
    for _ in range(count):
        transaction = generator.generate_transaction()
        send_transaction(transaction)


if __name__ == "__main__":
    main()
