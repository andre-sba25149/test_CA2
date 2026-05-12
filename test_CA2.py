import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


groceries_df = pd.read_csv("Groceries_dataset.csv")
top_item = pd.read_csv("Groceries_dataset.csv")
item = top_item['itemDescription'].value_counts().head(10)

client = groceries_df['Member_number'].value_counts().head(10)


top_item['Date'] = pd.to_datetime(top_item['Date'], dayfirst=True)


top_item = top_item.sort_values('Date')

top_item['Date'] = top_item['Date'].dt.strftime('%d-%m-%Y')

basket_item = top_item.copy()

basket_item = basket_item.groupby(["Member_number", "Date"], as_index=False)["itemDescription"].count()

basket_item = basket_item.rename(columns={"itemDescription":"basket_item"})


bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, float('inf')]
labels = ['1-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '40+']
basket_item['basket_item'] = pd.cut(basket_item['basket_item'], bins=bins, labels=labels)


basket_item['Date'] = pd.to_datetime(basket_item['Date'], dayfirst=True)

basket_item = basket_item.sort_values('Date')



dash_3 = pd.read_csv("Groceries_dataset.csv")
dash_3['Date'] = pd.to_datetime(dash_3['Date'], dayfirst=True)



daily_summary = dash_3.groupby('Date')['itemDescription'].count().reset_index()
daily_summary.columns = ['Date', 'total_sold']

daily_summary = daily_summary.sort_values('Date')
daily_summary['Date'] = daily_summary['Date'].dt.strftime('%d-%m-%Y')


daily_summary['Date'] = pd.to_datetime(daily_summary['Date'], dayfirst=True)

monthly_data = daily_summary.set_index('Date')


monthly_summary = monthly_data['total_sold'].resample('ME').sum().reset_index()
monthly_summary['Date'] = monthly_summary['Date'].dt.to_period('M')




st.title('Online Retail Data Summary')

data=top_item
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