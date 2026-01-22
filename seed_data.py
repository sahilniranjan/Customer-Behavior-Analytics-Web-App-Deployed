"""
Seed the database with demo data for recruiters.
This ensures the dashboard always has data to display.
"""

from datetime import datetime, timedelta
import random
from database import db, UserInteraction
from app import app


def seed_demo_data():
    """Generate and insert demo data into the database."""
    
    # Check if data already exists
    with app.app_context():
        existing_count = UserInteraction.query.count()
        if existing_count > 0:
            print(f"Database already has {existing_count} interactions. Skipping seed.")
            return
        
        print("Seeding database with demo data...")
        
        user_ids = [f"demo_user_{i:03d}" for i in range(1, 31)]
        actions = ["page_view", "click", "scroll", "hover", "submit", "search", "download", "add_to_cart", "checkout"]
        pages = ["/home", "/products", "/about", "/contact", "/pricing", "/features", "/blog", "/dashboard", "/profile"]
        devices = ["desktop", "mobile", "tablet"]
        referrers = ["google", "facebook", "direct", "twitter", "linkedin", "reddit"]
        
        interactions = []
        
        # Generate data for the last 30 days
        base_date = datetime.utcnow() - timedelta(days=30)
        
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            # More interactions on recent days
            num_interactions = random.randint(20, 50) + (day * 2)
            
            for _ in range(num_interactions):
                interaction = UserInteraction(
                    user_id=random.choice(user_ids),
                    action=random.choice(actions),
                    page=random.choice(pages),
                    meta_data={
                        "session_duration": random.randint(10, 600),
                        "device": random.choice(devices),
                        "referrer": random.choice(referrers),
                        "scroll_depth": random.randint(10, 100),
                        "clicks": random.randint(1, 20)
                    },
                    timestamp=current_date + timedelta(
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                )
                interactions.append(interaction)
        
        # Bulk insert
        db.session.bulk_save_objects(interactions)
        db.session.commit()
        
        print(f"✅ Successfully seeded {len(interactions)} interactions!")
        print("Dashboard is now ready with sample data.")


if __name__ == "__main__":
    seed_demo_data()
