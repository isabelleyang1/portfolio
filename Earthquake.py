#!/usr/bin/env python
# coding: utf-8

# In[105]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os


# In[106]:


directory_path = '/Users/isabelleyang/Desktop/Projects/Earthquakes'
os.chdir(directory_path)


# In[107]:


df = pd.read_csv('QuakesToday.csv')


# In[108]:


df


# In[109]:


# Check for missing values in the DataFrame
missing_values = df.isnull().sum()
print(missing_values)


# In[110]:


# Check for duplicate records in the DataFrame
duplicates = df.duplicated()
print(duplicates)


# In[111]:


# Drop the duplicate records from the DataFrame
df = df.drop_duplicates()


# In[112]:


# Split the "datetime" column into "date" and "time" columns
df[['Date', 'Time']] = df['Datetime'].str.split(' ', expand=True)


# In[113]:


#Drop the "Username" column
df = df.drop('Username', axis=1)


# In[114]:


# Split the "Date" column into "Year", "Month", and "Day"
df['Year'], df['Month'], df['Day'] = df['Date'].str.split('-', 2).str


# In[115]:


# Extract the "Hour" from the "Time" column
df['Hour'] = pd.to_datetime(df['Time']).dt.hour


# In[116]:


# Extract the "Magnitude" from the "Text" column (using code from previous response)
df['Magnitude'] = df['Text'].str.extract(r'(\d+(?:\.\d+)?)\s*magnitude').astype(float)


# In[117]:


#Create a new column for hashtags
df['Hashtags'] = df['Text'].str.findall(r'#(\w+)')


# In[118]:


# Create a new column for the extracted location
df['Location'] = df['Text'].str.extract(r'(\d+\s*km\s*from|ESE\s*of)?\s*([\w\s]+),', expand=False)[1]


# In[119]:


# Remove whitespaces from the Location column
df['Location'] = df['Location'].str.strip()


# In[120]:


#Calculate basic statistics for the magnitude column
magnitude_stats = df['Magnitude'].describe()
magnitude_stats


# In[121]:


# Histogram
plt.hist(df['Magnitude'], bins=10, edgecolor='black')
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.title('Distribution of Earthquake Magnitudes')
plt.show()


# In[122]:


monthly_avg = df.groupby('Month')['Magnitude'].mean()
# Scatter plot of magnitudes over time
plt.plot(monthly_avg.index, monthly_avg.values)
plt.xlabel('Month')
plt.ylabel('Magnitude')
plt.title('Monthly Average Earthquake Magnitude')
for x, y in zip(monthly_avg.index, monthly_avg.values):
    plt.text(x, y, round(y, 2), ha='center', va='bottom')

plt.show()


# In[123]:


# Bar plot of count by magnitude range
magnitude_ranges = pd.cut(df['Magnitude'], bins=[0, 2, 4, 6, 8, 10])
magnitude_counts = magnitude_ranges.value_counts().sort_index()
plt.bar(magnitude_counts.index.astype(str), magnitude_counts.values)
plt.xlabel('Magnitude Range')
plt.ylabel('Count')
plt.title('Count of Earthquakes by Magnitude Range')
plt.show()


# In[124]:


monthly_count = df['Month'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=monthly_count.index, y=monthly_count.values)
plt.xlabel('Month')
plt.ylabel('Earthquake Count')
plt.title('Monthly Distribution of Earthquakes')
plt.show()


# In[125]:


daily_count = df['Day'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=daily_count.index, y=daily_count.values)
plt.xlabel('Day')
plt.ylabel('Earthquake Count')
plt.title('Daily Distribution of Earthquakes')
plt.show()


# In[126]:


hourly_count = df['Hour'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=hourly_count.index, y=hourly_count.values)
plt.xlabel('Hour')
plt.ylabel('Earthquake Count')
plt.title('Hourly Distribution of Earthquakes')
plt.show()


# In[127]:


# Extract all unique hashtags from the dataset
all_hashtags = set(tag for tags in df['Hashtags'] for tag in tags)

# Count the occurrence of each hashtag
hashtag_counts = {}
for hashtags in df['Hashtags']:
    for tag in hashtags:
        hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1

# Sort the hashtags based on their counts in descending order
sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)


# In[128]:


# Select the top 10 hashtags
top_n = 10
top_hashtags = sorted_hashtags[:top_n]

# Extract the hashtags and their corresponding counts
hashtags = [tag for tag, count in top_hashtags]
counts = [count for tag, count in top_hashtags]

# Create a bar plot to visualize the top hashtags
plt.bar(hashtags, counts)
plt.xlabel('Hashtags')
plt.ylabel('Count')
plt.title('Top {} Hashtags'.format(top_n))
plt.xticks(rotation=45)
plt.show()


# In[129]:


correlation_matrix = df[['Magnitude', 'Year', 'Month', 'Day', 'Hour']].corr()
print(correlation_matrix)


# In[130]:


#The correlation coefficient between "Magnitude" and "Hour" is -0.038246. 
#This value is close to zero, indicating a weak or negligible correlation between the two variables. 
#The negative sign suggests a slight inverse relationship, but the correlation is not significant.

