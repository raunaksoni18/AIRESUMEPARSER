from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(texts):
    """Convert texts to semantic embeddings."""
    return model.encode(texts)

def cluster_skills(skill_phrases, n_clusters=5):
    """Cluster skills into categories."""
    if len(skill_phrases) < 2:
        return np.array([0] * len(skill_phrases))
    
    embeddings = get_embeddings(skill_phrases)
    kmeans = KMeans(n_clusters=min(n_clusters, len(skill_phrases)), random_state=42)
    clusters = kmeans.fit_predict(embeddings)
    return clusters
