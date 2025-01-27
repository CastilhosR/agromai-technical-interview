"""
Question 3: Sales Visualization

Using the cleaned dataset from Question 1 ('sales_data.csv'), create the following visualizations:

1. Create a line plot showing daily sales trends over time
   - Include a 7-day moving average line

2. Create a bar plot showing:
   - Total sales by category
   - Include error bars representing standard deviation

3. Create a scatter plot showing:
   - Relationship between quantity and price
   - Color points by category
   - Add a trend line

Requirements:
- Use appropriate labels and titles
- Include a legend where necessary
- Use a consistent color scheme
- Save all plots as PNG files
"""

#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import pickle

df_raw = pickle.load(open('./data/sales_data.pkl', 'rb'))

df_raw.set_index('sale_date', inplace=True)

df1["total_sales"] = df1["price"] * df1["quantity"]

df1['7_day_avg'] = df1['total_sales'].rolling(window=7).mean()

# 1. Linhas com tendência de vendas diárias e média móvel de 7 dias
fig1 = go.Figure()

fig1.add_trace(go.Scatter(x=df1.index, y=df1['total_sales'], mode='lines', name='Vendas Diárias'))
fig1.add_trace(go.Scatter(x=df1.index, y=df1['7_day_avg'], mode='lines', name='Média Móvel de 7 Dias', line=dict(dash='dash')))

# Personalizando o gráfico
fig1.update_layout(
    title='Tendência Diária de Vendas',
    xaxis_title='Data',
    yaxis_title='Vendas Totais',
    template='plotly',
    legend_title="Legenda",
    height=600
)
# fig1.show();

# Salvando o gráfico como PNG
fig1.write_image("sales_trend.png")

# 2. Barras com vendas totais por categoria e barras de erro (desvio padrão)

category_sales = df1.groupby('category')['total_sales'].sum()
category_std = df1.groupby('category')['total_sales'].std()

# Criando o gráfico de barras
fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=category_sales.index,
    y=category_sales,
    name='Vendas Totais',
    error_y=dict(type='data', array=category_std, visible=True)
))

# Personalizando o gráfico
fig2.update_layout(
    title='Vendas Totais por Categoria',
    xaxis_title='Categoria',
    yaxis_title='Vendas Totais',
    template='plotly',
    legend_title="Legenda",
    height=600
)
# fig2.show();

# Salvando o gráfico como PNG
fig2.write_image("category_sales.png")

# 3. Scatter de quantidade e preço, colorido por categoria e com linha de tendência (ficou estranho)

fig3 = px.scatter(df1, x='quantity', y='price', color='category', trendline="ols", 
                  title='Relação entre Quantidade e Preço', labels={'quantity': 'Quantidade', 'price': 'Preço'})

# Personalizando o gráfico
fig3.update_layout(
    title='Relação entre Quantidade e Preço',
    xaxis_title='Quantidade',
    yaxis_title='Preço',
    template='plotly',
    legend_title="Categoria",
    height=600
)
# fig3.show();

# Salvando o gráfico como PNG
fig3.write_image("quantity_price_relationship.png")
