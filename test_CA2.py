import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Setup Data
st.set_page_config(layout="wide")
st.title('Online Retail Data Summary')

# (Assume 'data', 'monthly_summary', and 'basket_item' are loaded here)

# 2. Sidebar Filters (Replacing the Tkinter Combobox)
years = sorted(data['Date'].dt.year.unique().tolist())
selected_year = st.sidebar.selectbox('Filter by year', ['All'] + [str(y) for y in years])

# 3. Filtering Logic
if selected_year == 'All':
    df1, df2, df3 = data, monthly_summary, basket_item
else:
    y = int(selected_year)
    df1 = data[data['Date'].dt.year == y]
    df2 = monthly_summary[monthly_summary['Date'].dt.year == y]
    df3 = basket_item[basket_item['Date'].dt.year == y]

# 4. Metrics (Replacing the Labels)
col1, col2 = st.columns(2)
col1.metric("Total items sold", df1['itemDescription'].count())
col2.metric("Total items available", df1['itemDescription'].nunique())

# 5. Charts (Replacing FigureCanvasTkAgg)
c1, c2, c3 = st.columns(3)

with c1:
    fig1, ax1 = plt.subplots()
    df1['itemDescription'].value_counts().head(5).plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

with c2:
    fig2, ax2 = plt.subplots()
    df3['basket_item'].value_counts().head(5).plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

with c3:
    fig3, ax3 = plt.subplots()
    df2.plot(kind='line', x='Date', y='total_sold', ax=ax3)
    st.pyplot(fig3)