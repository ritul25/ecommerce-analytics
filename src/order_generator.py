import mysql.connector
import random
import time
from datetime import datetime


# ==========================================
# MySQL Connection
# ==========================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9720341009",
    database="ecommerce_analytics"
)

cursor = db.cursor(dictionary=True)

print("========================================")
print(" Dynamic E-Commerce Order Generator")
print("========================================")
print("Generator started successfully...")
print("1-2 new orders will be generated every minute.")
print("Stock will be updated automatically.")
print("Press CTRL+C to stop.\n")


# ==========================================
# Generate Order
# ==========================================

def generate_order():

    try:

        # ----------------------------------
        # Get random customer
        # ----------------------------------

        cursor.execute("""
            SELECT customer_id
            FROM customers
            ORDER BY RAND()
            LIMIT 1
        """)

        customer = cursor.fetchone()

        if not customer:
            print("No customers found.")
            return

        customer_id = customer["customer_id"]


        # ----------------------------------
        # Get random product with stock
        # ----------------------------------

        cursor.execute("""
            SELECT
                product_id,
                selling_price,
                cost_price,
                stock_quantity
            FROM products
            WHERE stock_quantity > 0
            ORDER BY RAND()
            LIMIT 1
        """)

        product = cursor.fetchone()

        if not product:
            print("No products with available stock.")
            return


        product_id = product["product_id"]
        unit_price = float(product["selling_price"])
        cost_price = float(product["cost_price"])
        available_stock = product["stock_quantity"]


        # ----------------------------------
        # Random quantity
        # ----------------------------------

        quantity = random.randint(
            1,
            min(3, available_stock)
        )


        # ----------------------------------
        # Random discount
        # ----------------------------------

        discount = random.choice([
            0,
            0,
            0,
            5,
            10,
            15
        ])


        # ----------------------------------
        # Calculate sales
        # ----------------------------------

        gross_amount = unit_price * quantity

        discount_amount = gross_amount * discount / 100

        sales_amount = gross_amount - discount_amount

        cost = cost_price * quantity

        profit = sales_amount - cost


        # ----------------------------------
        # Payment method
        # ----------------------------------

        payment_method = random.choice([
            "UPI",
            "Credit Card",
            "Debit Card",
            "COD",
            "Net Banking",
            "Wallet"
        ])


        # ----------------------------------
        # Order status
        # ----------------------------------

        order_status = random.choices(
            [
                "Pending",
                "Confirmed",
                "Shipped",
                "Delivered",
                "Cancelled",
                "Returned"
            ],
            weights=[
                5,
                10,
                15,
                55,
                10,
                5
            ]
        )[0]


        # ----------------------------------
        # Current date & time
        # ----------------------------------

        now = datetime.now()

        order_date = now.date()
        order_time = now.time()


        # ==================================
        # Start MySQL Transaction
        # ==================================


        # ----------------------------------
        # Insert Order
        # ----------------------------------

        order_sql = """
            INSERT INTO orders
            (
                customer_id,
                product_id,
                order_date,
                order_time,
                quantity,
                unit_price,
                discount,
                sales_amount,
                cost,
                profit,
                payment_method,
                order_status
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """

        order_values = (
            customer_id,
            product_id,
            order_date,
            order_time,
            quantity,
            unit_price,
            discount,
            sales_amount,
            cost,
            profit,
            payment_method,
            order_status
        )

        cursor.execute(order_sql, order_values)


        # ----------------------------------
        # Update Product Stock
        # ----------------------------------

        stock_sql = """
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE product_id = %s
            AND stock_quantity >= %s
        """

        cursor.execute(
            stock_sql,
            (
                quantity,
                product_id,
                quantity
            )
        )


        # ----------------------------------
        # Check stock update
        # ----------------------------------

        if cursor.rowcount == 0:

            db.rollback()

            print(
                f"Stock changed before order could be completed "
                f"for Product {product_id}"
            )

            return


        # ----------------------------------
        # Commit transaction
        # ----------------------------------

        db.commit()


        # ==================================
        # Success Message
        # ==================================

        new_stock = available_stock - quantity

        print(
            f"[{now.strftime('%H:%M:%S')}] "
            f"Order #{cursor.lastrowid} generated | "
            f"Customer: {customer_id} | "
            f"Product: {product_id} | "
            f"Qty: {quantity} | "
            f"Sales: ₹{sales_amount:.2f} | "
            f"Profit: ₹{profit:.2f} | "
            f"Status: {order_status} | "
            f"Remaining Stock: {new_stock}"
        )


    except Exception as e:

        db.rollback()

        print("Error:", e)


# ==========================================
# Continuous Generator
# ==========================================

try:

    while True:

        # Randomly generate 1 or 2 orders
        number_of_orders = random.randint(1, 2)

        for _ in range(number_of_orders):

            generate_order()

        print("Waiting for next cycle...\n")

        # Wait 60 seconds
        time.sleep(60)


except KeyboardInterrupt:

    print("\n========================================")
    print(" Order generator stopped.")
    print("========================================")


finally:

    cursor.close()
    db.close()