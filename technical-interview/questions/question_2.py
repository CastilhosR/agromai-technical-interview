"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

Bonus: Identify any customers who haven't made a purchase in the last 3 months
"""
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import pickle

df_raw = pd.read_csv('./data/customer_purchases.csv')

l, c = df_raw.shape
print(f'{l} lihas e {c} colunas' )

df_raw['purchase_date'] = pd.to_datetime(df_raw['purchase_date'])

df1 = df_raw.copy()

customer_metrics = df1.groupby('customer_id').agg(
                   total_spent=('amount', 'sum'),
                   avg_purchase_value=('amount', 'mean'),
                   num_purchases=('purchase_id', 'count'),
                   most_frequent_category=('category', lambda x: x.mode()[0] if not x.mode().empty else None)
).reset_index()

top_5_customers = customer_metrics.nlargest(5, 'total_spent')
bottom_5_customers = customer_metrics.nsmallest(5, 'total_spent')

df1['month'] = df1['purchase_date'].dt.to_period('M')

monthly_trends = df1.groupby('month').agg(
                 total_sales=('amount', 'sum'),
                 avg_purchase_value=('amount', 'mean')
).reset_index()

latest_date = df1['purchase_date'].max()
three_months_ago = latest_date - pd.DateOffset(months=3)

inactive_customers = df1[df1['purchase_date'] <= three_months_ago]['customer_id'].unique()
active_customers = df1[df1['purchase_date'] > three_months_ago]['customer_id'].unique()
customers_no_recent_purchases = set(inactive_customers) - set(active_customers)

print("Customer Metrics:")
print(customer_metrics.head())

print("\nTop 5 customers - total amount:")
print(top_5_customers)

print("\nBottom 5 customers - total amount:")
print(bottom_5_customers)

print("\nPurchase Monthly Trends:")
print(monthly_trends)

print("\nCustomers without purchases in the last 3 months:")
print(customers_no_recent_purchases)

pickle.dump(df1, open('./data/customer_purchases.pkl', 'wb'))
