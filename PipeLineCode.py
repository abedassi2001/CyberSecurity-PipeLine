import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# 3. Feature distribution by class example for a few features
features_to_plot = ['UsingIP', 'LongURL', 'HTTPS']

for feature in features_to_plot:
    plt.figure(figsize=(6,4))
    sns.countplot(x=feature, hue='class', data=df)
    plt.title(f'Distribution of {feature} by Class')
    plt.show()

# Remove correlated features
features_to_remove = ['Favicon', 'UsingPopupWindow']

# Drop from dataset (excluding target and index)
X = df.drop(columns=['class', 'Index'] + features_to_remove)

# Optionally, create a cleaned dataframe including target
df_cleaned = pd.concat([X, df['class']], axis=1)

print(f"Removed features due to high correlation: {features_to_remove}")
print(f"Remaining features count: {X.shape[1]}")

# 4. Correlation heatmap
plt.figure(figsize=(14,12))
sns.heatmap(df.corr(), cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()

