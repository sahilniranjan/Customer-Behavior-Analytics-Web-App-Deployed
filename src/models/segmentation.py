"""
User segmentation based on activity features.
"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def segment_users(df: pd.DataFrame, n_clusters: int = 5):
    """
    Segment users into n_clusters based on their activity counts.
    Expects df columns: user_id, action, page, timestamp
    Returns: dict mapping segment_label to list of users
    """
    counts = df.groupby('user_id').size().reset_index(name='total_events')
    X = counts[['total_events']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(X_scaled)
    counts['segment'] = kmeans.labels_
    return counts.groupby('segment')['user_id'].apply(list).to_dict()
