"""
Question 1: Data Cleaning and Basic Analysis

Using the provided dataset 'sales_data.csv', perform the following tasks:

1. Load and examine the dataset
2. Clean the data:
   - Handle missing values in the 'price' column (replace with mean)
   - Handle missing values in the 'category' column (replace with mode)
   - Convert 'sale_date' to datetime
3. Create a summary of:
   - Total number of sales per category
   - Average price per category
   - Number of missing values handled

The cleaned dataset should be ready for further analysis.
"""

#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

df_raw = pd.read_csv('./data/sales_data.csv')

l, c = df_raw.shape
print(f'{l} lihas e {c} colunas' )

df_raw['sale_date'] = pd.to_datetime(df_raw["sale_date"])

columns_with_null = df_raw.columns[df_raw.isnull().any()].tolist()

missing_values = {}

for col in columns_with_null:
    missing_values[col] = df_raw[col].isna().sum()

aux1 = df_raw['category'].value_counts().idxmax()

df1 = df_raw.copy()

df1['category'] = df1['category'].fillna(aux1)

cats = df1['category'].unique()

vendas_cat = df1.groupby('category')['sale_id'].count()

preco_medio_cat = df1.groupby('category')['price'].mean()

df1['price'] = df1.apply(lambda row: preco_medio_cat.get(row['category']) if pd.isna(row['price']) else row['price'], axis=1)

print("Total Number of Sales per Category:")
print(vendas_cat)

print("\nAverage Price per Category:")
print(preco_medio_cat)

print("\nMissing Values Handled:")
print(missing_values)

pickle.dump(df1, open('./data/sales_data.pkl', 'wb'))