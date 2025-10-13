"""
Simple churn prediction using logistic regression.
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression

def predict_churn(df: pd.DataFrame, feature_cols: list):
    """
    Trains and returns churn probability for each user.
    Expects df with feature_cols and 'churned' column.
    """
    X = df[feature_cols]
    y = df['churned']
    model = LogisticRegression().fit(X, y)
    preds = model.predict_proba(X)[:,1]
    return dict(zip(df['user_id'], preds))
