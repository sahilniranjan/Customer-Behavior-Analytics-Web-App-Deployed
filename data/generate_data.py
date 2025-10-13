"""
Script to generate synthetic customer interaction data.
Produces a CSV file simulating user events over time.
"""
import csv
import random
from datetime import datetime, timedelta

OUTPUT_FILE = 'data/interactions.csv'
NUM_USERS = 100
NUM_EVENTS = 10000

actions = ['page_view', 'click', 'purchase', 'signup']
pages = ['/home', '/products', '/cart', '/checkout', '/signup']

with open(OUTPUT_FILE, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_id', 'action', 'page', 'timestamp', 'metadata'])
    start = datetime.utcnow() - timedelta(days=30)
    for _ in range(NUM_EVENTS):
        user = f'user_{random.randint(1, NUM_USERS)}'
        action = random.choice(actions)
        page = random.choice(pages)
        time = start + timedelta(seconds=random.randint(0, 30*24*3600))
        metadata = {'value': random.random(), 'session': random.randint(1,5000)}
        writer.writerow([user, action, page, time.isoformat(), metadata])

print(f"Generated {NUM_EVENTS} events to {OUTPUT_FILE}")
