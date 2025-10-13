"""
Recommendation engine based on collaborative filtering.
"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_items(df: pd.DataFrame, user_id: str, top_n: int = 5):
    """
    Recommend items/pages for a user based on others' interactions.
    Expects df columns: user_id, page, count
    """
    pivot = df.pivot_table(index='user_id', columns='page', values='count', fill_value=0)
    sim = cosine_similarity(pivot)
    idx = list(pivot.index).index(user_id)
    scores = list(enumerate(sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    recs = []
    for i, score in scores[1:top_n+1]:
        page = pivot.index[i]
        recs.append({'page': page, 'score': float(score)})
    return recs
