from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class UserInteraction(db.Model):
    """Model for storing user interaction data."""
    
    __tablename__ = 'user_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    action = db.Column(db.String(100), nullable=False)
    page = db.Column(db.String(200), nullable=False)
    meta_data = db.Column('metadata', db.JSON, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<UserInteraction {self.id}: {self.user_id} - {self.action}>'
    
    def to_dict(self):
        """Convert interaction to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'page': self.page,
            'metadata': self.meta_data,
            'timestamp': self.timestamp.isoformat()
        }


class BehaviorPattern(db.Model):
    """Model for storing recognized behavioral patterns."""
    
    __tablename__ = 'behavior_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    pattern_type = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    pattern_details = db.Column('details', db.JSON, nullable=True)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BehaviorPattern {self.id}: {self.pattern_type} - {self.confidence}>'
    
    def to_dict(self):
        """Convert pattern to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pattern_type': self.pattern_type,
            'confidence': self.confidence,
            'details': self.pattern_details,
            'detected_at': self.detected_at.isoformat()
        }
