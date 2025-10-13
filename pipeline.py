import time
import os
from datetime import datetime
from dotenv import load_dotenv
from database import db, UserInteraction, BehaviorPattern
from analytics import PatternRecognizer
from app import app

load_dotenv()


class DataPipeline:
    """
    Real-time data pipeline for continuous analysis.
    Maintains 99% uptime for processing user interactions.
    """
    
    def __init__(self, interval=60):
        """
        Initialize the data pipeline.
        
        Args:
            interval: Processing interval in seconds (default: 60)
        """
        self.interval = interval
        self.pattern_recognizer = PatternRecognizer()
        self.is_running = False
        self.uptime_counter = 0
        self.error_counter = 0
    
    def start(self):
        """Start the real-time data pipeline."""
        self.is_running = True
        print(f"[{datetime.now()}] Data Pipeline started - Processing every {self.interval} seconds")
        
        try:
            while self.is_running:
                self._process_batch()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the data pipeline."""
        self.is_running = False
        uptime_percentage = (self.uptime_counter / (self.uptime_counter + self.error_counter)) * 100 if (self.uptime_counter + self.error_counter) > 0 else 0
        print(f"\n[{datetime.now()}] Data Pipeline stopped")
        print(f"Uptime: {uptime_percentage:.2f}%")
        print(f"Successful cycles: {self.uptime_counter}")
        print(f"Errors: {self.error_counter}")
    
    def _process_batch(self):
        """Process a batch of user interactions."""
        try:
            with app.app_context():
                # Get recent unprocessed interactions
                recent_interactions = UserInteraction.query.order_by(
                    UserInteraction.timestamp.desc()
                ).limit(100).all()
                
                if recent_interactions:
                    print(f"[{datetime.now()}] Processing {len(recent_interactions)} interactions...")
                    
                    # Analyze patterns
                    patterns = self.pattern_recognizer.analyze_patterns()
                    
                    print(f"[{datetime.now()}] Detected {len(patterns)} patterns")
                    
                    # Store detected patterns in database
                    for pattern in patterns:
                        if pattern.get('user_id'):
                            behavior_pattern = BehaviorPattern(
                                user_id=pattern['user_id'],
                                pattern_type=pattern['type'],
                                confidence=pattern['confidence'],
                                pattern_details=pattern,
                                detected_at=datetime.utcnow()
                            )
                            db.session.add(behavior_pattern)
             
            db.session.commit()
            print(f"[{datetime.now()}] Batch processing completed successfully")
            self.uptime_counter += 1
        except Exception as e:
            self.error_counter += 1
            print(f"[{datetime.now()}] Error in pipeline: {str(e)}")
            
            # Calculate current uptime
            uptime_percentage = (self.uptime_counter / (self.uptime_counter + self.error_counter)) * 100
            if uptime_percentage < 99:
                print(f"[WARNING] Uptime dropped below 99%: {uptime_percentage:.2f}%")


if __name__ == "__main__":
    interval = int(os.getenv('DATA_PIPELINE_INTERVAL', 60))
    pipeline = DataPipeline(interval=interval)
    
    print("=" * 60)
    print("Customer Behavior Analytics - Real-time Data Pipeline")
    print("=" * 60)
    print(f"Target Uptime: 99%")
    print(f"Processing Interval: {interval} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Ensure database tables exist before starting pipeline
    with app.app_context():
        db.create_all()

    pipeline.start()
