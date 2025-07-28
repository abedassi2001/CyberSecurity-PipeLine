import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

# Load data
df = pd.read_csv('phishing.csv')

# 1. Class distribution
plt.figure(figsize=(6,4))
sns.countplot(x='class', data=df)
plt.title('Class Distribution: Legitimate (1) vs Phishing (-1)')
plt.show()

# 2. Feature presence rate (proportion of 1s)
feature_cols = df.columns.drop(['class', 'Index'])
feature_means = df[feature_cols].mean().sort_values(ascending=False)

plt.figure(figsize=(12,6))
feature_means.plot(kind='bar')
plt.title('Feature Presence Rate (Proportion of 1s per feature)')
plt.ylabel('Proportion of 1s')
plt.show()

# 3. Feature distribution by class (example for a few features)
features_to_plot = ['UsingIP', 'LongURL', 'HTTPS']
for feature in features_to_plot:
    plt.figure(figsize=(6,4))
    sns.countplot(x=feature, hue='class', data=df)
    plt.title(f'Distribution of {feature} by Class')
    plt.show()

# 4. Remove highly correlated features
features_to_remove = ['Favicon', 'UsingPopupWindow']
X = df.drop(columns=['class', 'Index'] + features_to_remove)
y = df['class']

# 5. Outlier detection using Isolation Forest
iso = IsolationForest(contamination=0.01, random_state=42)
outlier_flags = iso.fit_predict(X)

# Add outlier label: -1 = outlier, 1 = inlier
df['outlier'] = outlier_flags

# Remove outliers
df_no_outliers = df[df['outlier'] == 1].drop(columns=['outlier'])
print(f"\nOutliers removed: {df.shape[0] - df_no_outliers.shape[0]}")
print(f"Remaining samples: {df_no_outliers.shape[0]}")

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

# Use cleaned data without 'class', 'Index', 'Favicon', and 'UsingPopupWindow'
X = df.drop(columns=['class', 'Index', 'Favicon', 'UsingPopupWindow'])

# Apply KMeans clustering (2 clusters expected: phishing vs legit)
kmeans = KMeans(n_clusters=2, random_state=42)
clusters = kmeans.fit_predict(X)

# Add cluster label to dataframe
df['Cluster'] = clusters

# PCA for visualization (reduce to 2D)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=df['Cluster'], palette='Set2')
plt.title("KMeans Clustering – Pattern Recognition")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.show()
