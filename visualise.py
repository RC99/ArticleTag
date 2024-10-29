import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the first dataset to get the column labels
first_df = pd.read_excel('Labeled_Data/scraped_articles_business_2_with_sentiment.xlsx')
columns = first_df.columns  # Extract column names

# Load all sheets and concatenate using the columns from the first dataset
sheets = ['Labeled_Data/scraped_articles_business_2_with_sentiment.xlsx', 'Labeled_Data/scraped_articles_business1_with_sentiment.xlsx'
          , 'Labeled_Data/scraped_articles_tech_with_sentiment.xlsx', 'Labeled_Data/scraped_articles_with_sentiment.xlsx']
dfs = [pd.read_excel(sheet, names=columns) for sheet in sheets]  # Use the same column names
df = pd.concat(dfs, ignore_index=True)
print(df.tail())
# Data Cleaning
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

from sklearn.utils import resample
positive = df[df['sentiment'] == 'positive']
negative = df[df['sentiment'] == 'negative']
neutral = df[df['sentiment'] == 'neutral']

negative_upsampled = resample(negative, replace=True, n_samples=len(positive), random_state=42)
neutral_upsampled = resample(neutral, replace=True, n_samples=len(positive), random_state=42)

df_upsampled = pd.concat([positive, negative_upsampled, neutral_upsampled])

print(df_upsampled['sentiment'].value_counts())

# Visualization
plt.figure(figsize=(12, 6))
sns.countplot(x='class', data=df, palette="viridis")
plt.title('Count of Articles by Category')
plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x='sentiment', data=df, palette="coolwarm")
plt.title('Count of Articles by Sentiment')
plt.show()

# Category Distribution Pie Chart
category_counts = df['class'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("viridis"))
plt.title('Category Distribution')
plt.show()

# Sentiment Distribution Pie Chart
sentiment_counts = df['sentiment'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("coolwarm"))
plt.title('Sentiment Distribution')
plt.show()

# Joint Distribution Heatmap
category_sentiment_counts = df.groupby(['class', 'sentiment']).size().unstack()
plt.figure(figsize=(10, 6))
sns.heatmap(category_sentiment_counts, annot=True, fmt="d", cmap="YlGnBu")
plt.title('Heatmap of Sentiment by Category')
plt.show()

category_counts = df_upsampled['class'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("viridis"))
plt.title('Category Distribution')
plt.show()