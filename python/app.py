import socket
import json
import time
import random
from faker import Faker

fake = Faker()
host = "localhost"  # instead of "logstash"
port = 5000

products = ["Shoes", "T-Shirt", "Laptop", "Bag", "Watch", "Bottle"]
payments = ["Credit Card", "PayPal", "Apple Pay", "Google Pay"]
status_list = ["completed", "pending", "failed"]
errors = ["Payment gateway timeout", "Cart service crash", "Inventory service unavailable"]

sock = socket.socket()
sock.connect((host, port))

try:
    while True:
        if random.random() < 0.15:  # ~15% chance to log an error
            log = {
                "timestamp": fake.iso8601(),
                "level": "error",
                "message": random.choice(errors),
                "service": random.choice(["checkout", "cart", "inventory"]),
                "user_id": fake.uuid4()
            }
        else:
            log = {
                "timestamp": fake.iso8601(),
                "user_id": fake.uuid4(),
                "city": fake.city(),
                "product": random.choice(products),
                "price": round(random.uniform(10, 500), 2),
                "quantity": random.randint(1, 5),
                "payment_type": random.choice(payments),
                "status": random.choice(status_list)
            }

        sock.send((json.dumps(log) + "\n").encode("utf-8"))
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped sending logs.")
    sock.close()
