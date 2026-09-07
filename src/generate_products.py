import mysql.connector
import random
from datetime import date, timedelta

# -----------------------------
# MySQL Connection
# -----------------------------
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9720341009",
    database="ecommerce_analytics"
)

cursor = connection.cursor()

# -----------------------------
# Product Categories
# -----------------------------
product_catalog = {
    "Electronics": {
        "sub_categories": ["Laptops", "Mobiles", "Headphones", "Accessories"],
        "brands": ["HP", "Dell", "Lenovo", "Samsung", "Sony", "Boat"]
    },
    "Fashion": {
        "sub_categories": ["Shoes", "T-Shirts", "Jeans", "Watches"],
        "brands": ["Nike", "Adidas", "Puma", "Levis", "Roadster"]
    },
    "Home & Kitchen": {
        "sub_categories": ["Cookware", "Furniture", "Appliances", "Storage"],
        "brands": ["Prestige", "Philips", "IKEA", "Bajaj", "Havells"]
    },
    "Beauty": {
        "sub_categories": ["Skincare", "Haircare", "Makeup", "Fragrance"],
        "brands": ["Lakme", "Nivea", "Dove", "Maybelline", "Mamaearth"]
    },
    "Sports": {
        "sub_categories": ["Cricket", "Fitness", "Football", "Outdoor"],
        "brands": ["Adidas", "Nike", "Puma", "Yonex", "Cosco"]
    },
    "Books": {
        "sub_categories": ["Programming", "Education", "Fiction", "Business"],
        "brands": ["Penguin", "Oxford", "McGraw", "Pearson"]
    },
    "Grocery": {
        "sub_categories": ["Snacks", "Beverages", "Staples", "Packaged Food"],
        "brands": ["Tata", "Nestle", "Britannia", "Haldiram", "ITC"]
    }
}

# -----------------------------
# Product Name Templates
# -----------------------------
product_names = {
    "Laptops": ["Business Laptop", "Gaming Laptop", "Student Laptop", "Ultrabook"],
    "Mobiles": ["5G Smartphone", "Android Smartphone", "Budget Smartphone"],
    "Headphones": ["Wireless Headphones", "Bluetooth Earbuds", "Gaming Headset"],
    "Accessories": ["Wireless Mouse", "Mechanical Keyboard", "USB Hub", "Laptop Stand"],

    "Shoes": ["Running Shoes", "Sports Shoes", "Casual Sneakers"],
    "T-Shirts": ["Cotton T-Shirt", "Oversized T-Shirt", "Polo T-Shirt"],
    "Jeans": ["Slim Fit Jeans", "Regular Jeans", "Denim Jeans"],
    "Watches": ["Smart Watch", "Analog Watch", "Digital Watch"],

    "Cookware": ["Non Stick Pan", "Pressure Cooker", "Cookware Set"],
    "Furniture": ["Office Chair", "Study Table", "Bookshelf"],
    "Appliances": ["Mixer Grinder", "Electric Kettle", "Air Fryer"],
    "Storage": ["Storage Box", "Kitchen Organizer", "Plastic Container"],

    "Skincare": ["Face Wash", "Moisturizer", "Sunscreen"],
    "Haircare": ["Shampoo", "Hair Oil", "Conditioner"],
    "Makeup": ["Lipstick", "Foundation", "Compact Powder"],
    "Fragrance": ["Perfume", "Body Spray", "Deodorant"],

    "Cricket": ["Cricket Bat", "Cricket Ball", "Batting Gloves"],
    "Fitness": ["Yoga Mat", "Dumbbells", "Resistance Band"],
    "Football": ["Football", "Football Shoes", "Goalkeeper Gloves"],
    "Outdoor": ["Camping Tent", "Hiking Bag", "Water Bottle"],

    "Programming": ["Python Programming Book", "SQL Guide", "Data Analytics Book"],
    "Education": ["Mathematics Book", "Computer Science Book", "Exam Preparation Book"],
    "Fiction": ["Fiction Novel", "Mystery Novel", "Classic Novel"],
    "Business": ["Business Strategy Book", "Marketing Book", "Finance Book"],

    "Snacks": ["Potato Chips", "Namkeen", "Cookies"],
    "Beverages": ["Green Tea", "Coffee", "Juice"],
    "Staples": ["Rice", "Wheat Flour", "Pulses"],
    "Packaged Food": ["Instant Noodles", "Breakfast Cereal", "Ready To Eat"]
}

# -----------------------------
# Generate Products
# -----------------------------
products = []

for product_id in range(1, 501):

    category = random.choice(list(product_catalog.keys()))

    sub_category = random.choice(
        product_catalog[category]["sub_categories"]
    )

    brand = random.choice(
        product_catalog[category]["brands"]
    )

    base_name = random.choice(
        product_names[sub_category]
    )

    product_name = f"{brand} {base_name}"

    # Generate realistic prices
    cost_price = round(random.uniform(100, 50000), 2)

    selling_price = round(
        cost_price * random.uniform(1.10, 1.45),
        2
    )

    stock_quantity = random.randint(10, 500)

    rating = round(random.uniform(3.0, 5.0), 2)

    created_at = date.today() - timedelta(
        days=random.randint(0, 1000)
    )

    products.append((
        product_id,
        product_name,
        category,
        sub_category,
        brand,
        cost_price,
        selling_price,
        stock_quantity,
        rating,
        created_at
    ))

# -----------------------------
# Insert into MySQL
# -----------------------------
insert_query = """
INSERT INTO products
(
    product_id,
    product_name,
    category,
    sub_category,
    brand,
    cost_price,
    selling_price,
    stock_quantity,
    rating,
    created_at
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, products)

connection.commit()

print(f"{len(products)} products inserted successfully!")

cursor.close()
connection.close()