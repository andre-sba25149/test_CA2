import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- DATA LOADING ---
# (Ensure your data loading logic for top_item, monthly_summary etc. is here)
data = top_item 
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

st.title('Online Retail Data Summary')

# --- SIDEBAR FILTER (Replaces your Combobox) ---
years = sorted(data['Date'].dt.year.unique().tolist())
selected_year = st.sidebar.selectbox('Filter by year', ['All'] + [str(y) for y in years])

# --- FILTERING LOGIC ---
if selected_year == 'All':
    filtered_df = data
    filtered_df_2 = monthly_summary
    filtered_df_3 = basket_item
else:
    y_int = int(selected_year)
    filtered_df = data[data['Date'].dt.year == y_int]
    filtered_df_2 = monthly_summary[monthly_summary['Date'].dt.year == y_int]
    filtered_df_3 = basket_item[basket_item['Date'].dt.year == y_int]

# --- METRICS (Replaces your Labels) ---
col1, col2 = st.columns(2)
col1.metric("Total items sold", filtered_df['itemDescription'].count())
col2.metric("Total items available", filtered_df['itemDescription'].nunique())

# --- CHARTS (Replaces FigureCanvasTkAgg) ---
chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    fig1, ax1 = plt.subplots()
    filtered_df['itemDescription'].value_counts().head(5).plot(kind='bar', ax=ax1)
    ax1.set_title('Top selling items')
    st.pyplot(fig1)

with chart_col2:
    fig2, ax2 = plt.subplots()
    filtered_df_3['basket_item'].value_counts().head(5).plot(kind='bar', ax=ax2)
    ax2.set_title('Basket items quantity')
    st.pyplot(fig2)

with chart_col3:
    fig3, ax3 = plt.subplots()
    filtered_df_2.plot(kind='line', x='Date', y='total_sold', ax=ax3)
    ax3.set_title('Sales Over Time')
    st.pyplot(fig3)