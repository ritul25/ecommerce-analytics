import mysql.connector
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker("en_IN")

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
# Indian Locations
# -----------------------------
locations = {
    "Uttar Pradesh": ("North", ["Kasganj", "Kanpur", "Lucknow", "Agra", "Aligarh"]),
    "Delhi": ("North", ["New Delhi", "Delhi"]),
    "Haryana": ("North", ["Gurugram", "Faridabad", "Panipat"]),
    "Rajasthan": ("West", ["Jaipur", "Jodhpur", "Kota"]),
    "Maharashtra": ("West", ["Mumbai", "Pune", "Nagpur"]),
    "Gujarat": ("West", ["Ahmedabad", "Surat", "Vadodara"]),
    "West Bengal": ("East", ["Kolkata", "Siliguri"]),
    "Bihar": ("East", ["Patna", "Gaya", "Bhagalpur"]),
    "Tamil Nadu": ("South", ["Chennai", "Coimbatore", "Madurai"]),
    "Karnataka": ("South", ["Bengaluru", "Mysuru", "Mangalore"]),
    "Telangana": ("South", ["Hyderabad", "Warangal"]),
    "Kerala": ("South", ["Kochi", "Kozhikode", "Thiruvananthapuram"])
}

genders = ["Male", "Female", "Other"]

age_groups = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55+"
]

# -----------------------------
# Generate Customers
# -----------------------------
customers = []

for i in range(1, 1001):

    state = random.choice(list(locations.keys()))
    region, cities = locations[state]
    city = random.choice(cities)

    registration_date = date.today() - timedelta(
        days=random.randint(0, 1000)
    )

    customer = (
        i,
        fake.name(),
        random.choice(genders),
        random.choice(age_groups),
        city,
        state,
        region,
        registration_date
    )

    customers.append(customer)

# -----------------------------
# Insert into MySQL
# -----------------------------
insert_query = """
INSERT INTO customers
(
    customer_id,
    customer_name,
    gender,
    age_group,
    city,
    state,
    region,
    registration_date
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, customers)

connection.commit()

print(f"{len(customers)} customers inserted successfully!")

cursor.close()
connection.close()