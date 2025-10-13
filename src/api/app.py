"""
Flask API for analytics endpoints.
"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import UserInteraction, BehaviorPattern
from models.pattern_detection import detect_common_patterns
from models.churn_prediction import predict_churn
from models.recommendations import recommend_items
from models.segmentation import segment_users
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models (simplified)
# ...existing model definitions...

@app.route('/api/track', methods=['POST'])
def track_interaction():
    data = request.get_json()
    ui = UserInteraction(**data)
    db.session.add(ui)
    db.session.commit()
    return jsonify({'status':'success','id':ui.id}),201

@app.route('/api/analytics/patterns', methods=['GET'])
def api_patterns():
    df = pd.DataFrame([ui.to_dict() for ui in UserInteraction.query.all()])
    patterns = detect_common_patterns(df)
    return jsonify({'patterns':patterns}),200

@app.route('/api/analytics/trends', methods=['GET'])
def api_trends():
    df = pd.DataFrame([ui.to_dict() for ui in UserInteraction.query.all()])
    # simple trend: total per day
    df['date']=pd.to_datetime(df['timestamp']).dt.date
    trends = df.groupby('date').size().to_dict()
    return jsonify({'trends':trends}),200

@app.route('/api/analytics/churn', methods=['GET'])
def api_churn():
    df = pd.DataFrame([ui.to_dict() for ui in UserInteraction.query.all()])
    preds = predict_churn(df, ['some_feature'])
    return jsonify({'churn_predictions':preds}),200

@app.route('/api/analytics/segments', methods=['GET'])
def api_segments():
    df = pd.DataFrame([ui.to_dict() for ui in UserInteraction.query.all()])
    segments = segment_users(df)
    return jsonify({'segments':segments}),200

@app.route('/api/analytics/recommendations', methods=['GET'])
def api_recs():
    df = pd.DataFrame([ui.to_dict() for ui in UserInteraction.query.all()])
    page_counts = df.groupby(['user_id','page']).size().reset_index(name='count')
    recs = recommend_items(page_counts, request.args.get('user_id'))
    return jsonify({'recommendations':recs}),200

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)
