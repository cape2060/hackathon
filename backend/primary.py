import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.decomposition import LatentDirichletAllocation

# -------------------------------
# 1. LOAD YOUR DATASET
# -------------------------------
df = pd.read_csv('customer_sentiment_dataset.csv')

df = df.dropna(subset=['feedback', 'sentiment'])
df['feedback'] = df['feedback'].astype(str)

# -------------------------------
# 2. REPRESENTATIVE QUOTES
# -------------------------------
def get_representative_quotes(texts, n=5):
    """
    Pick n ‘medoid-like’ quotes by:
      1) building a TF-IDF matrix,
      2) computing pairwise cosine similarities,
      3) choosing the text with highest total similarity,
      4) then greedily picking next texts that maximize the minimum distance
         (1 – cosine) to any already chosen quote.
    """
    vec = TfidfVectorizer(stop_words='english')
    X = vec.fit_transform(texts)
    S = cosine_similarity(X)               # NxN matrix

    total_sim = S.sum(axis=1)
    selected = [int(total_sim.argmax())]   # first medoid

    for _ in range(1, n):
        dists = 1 - S[:, selected]
        min_dist = dists.min(axis=1)
        min_dist[selected] = -1
        chosen = int(min_dist.argmax())
        selected.append(chosen)

    return [texts[i] for i in selected]

pos_texts = df.loc[df.sentiment=='positive', 'feedback'].unique().tolist()
neg_texts = df.loc[df.sentiment=='negative', 'feedback'].unique().tolist()

top5_pos = get_representative_quotes(pos_texts, n=5)
top5_neg = get_representative_quotes(neg_texts, n=5)

print("Top 5 Positive Quotes:")
for q in top5_pos:
    print(" –", q)

print("\nTop 5 Negative Quotes:")
for q in top5_neg:
    print(" –", q)

# -------------------------------
# 3. PAIN POINTS DETECTION (IMPROVED)
# -------------------------------
# Use bigrams and trigrams for more context
cv = CountVectorizer(stop_words='english', ngram_range=(2,3), max_features=30)
Xn = cv.fit_transform(neg_texts)
scores_n = np.asarray(Xn.sum(axis=0)).ravel()
phrases_n = cv.get_feature_names_out()
top_pain_points = [phrases_n[i] for i in scores_n.argsort()[::-1][:10]]

# Define negative keywords for filtering
negative_keywords = [
    'not', 'no', 'poor', 'bad', 'terrible', 'broke', 'never', 'worst',
    'disappoint', 'problem', 'issue', 'fail', 'hate', 'awful', 'broken',
    'difficult', 'slow', 'unhappy', 'unacceptable', 'complain', 'refund'
]
filtered_pain_points = [p for p in top_pain_points if any(neg in p for neg in negative_keywords)]

print("\nTop Pain Points (filtered):")
for p in filtered_pain_points:
    print(" –", p)

# -------------------------------
# 4. POSITIVE POINTS DETECTION (IMPROVED)
# -------------------------------
# Use bigrams and trigrams for more context in positive feedback
cv_pos = CountVectorizer(stop_words='english', ngram_range=(2,3), max_features=30)
Xp_pos = cv_pos.fit_transform(pos_texts)
scores_pos = np.asarray(Xp_pos.sum(axis=0)).ravel()
phrases_pos = cv_pos.get_feature_names_out()
top_positive_points = [phrases_pos[i] for i in scores_pos.argsort()[::-1][:10]]

# Define positive keywords for filtering (optional)
positive_keywords = [
    'great', 'amazing', 'excellent', 'value', 'fast', 'recommend', 'satisfied',
    'love', 'best', 'happy', 'perfect', 'wonderful', 'pleased', 'awesome'
]
filtered_positive_points = [p for p in top_positive_points if any(pos in p for pos in positive_keywords)]

print("\nTop Positive Points (filtered):")
for p in filtered_positive_points:
    print(" –", p)

# -------------------------------
# 5. OPPORTUNITIES EXTRACTION
# -------------------------------
tfidf_pos = TfidfVectorizer(stop_words='english', max_features=20)
Xp = tfidf_pos.fit_transform(pos_texts)
scores_p = np.asarray(Xp.sum(axis=0)).ravel()
phrases_p = tfidf_pos.get_feature_names_out()
top5_opp = [phrases_p[i] for i in scores_p.argsort()[::-1][:5]]

print("\nBusiness Opportunities:")
for feat in top5_opp:
    print(f" – Opportunity: Enhance *{feat}*. Rationale: praised frequently in positive feedback.")





# pain points bar chart
freqs = [scores_n[phrases_n.tolist().index(p)] for p in filtered_pain_points]
plt.figure(figsize=(8,4))
plt.barh(filtered_pain_points[::-1], freqs[::-1])
plt.title("Top Pain-Point Keywords")
plt.xlabel("Count")
plt.show()



