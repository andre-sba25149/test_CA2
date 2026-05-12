import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. DATA LOADING & PREPARATION ---
# We load once and create our different summaries
raw_data = pd.read_csv("Groceries_dataset.csv")
raw_data['Date'] = pd.to_datetime(raw_data['Date'], dayfirst=True)

# Top Items Data
data = raw_data.copy().sort_values('Date')

# Basket Item Data
basket_item = data.groupby(["Member_number", "Date"], as_index=False)["itemDescription"].count()
basket_item = basket_item.rename(columns={"itemDescription":"basket_count"})

bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, float('inf')]
labels = ['1-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '40+']
basket_item['basket_bin'] = pd.cut(basket_item['basket_count'], bins=bins, labels=labels)

# Monthly Summary Data
# First get daily totals, then resample to Month End (ME)
daily_summary = data.groupby('Date')['itemDescription'].count().to_frame('total_sold')
monthly_summary = daily_summary.resample('ME').sum().reset_index()

# --- 2. SIDEBAR FILTER ---
st.title('Online Retail Data Summary')

years = sorted(data['Date'].dt.year.unique().tolist())
# We only need this ONCE.
selected_year = st.sidebar.selectbox(
    'Filter by year', 
    ['All'] + [str(y) for y in years], 
    key='year_selector'
)

# --- 3. FILTERING LOGIC ---
if selected_year == 'All':
    filtered_df = data
    filtered_df_2 = monthly_summary
    filtered_df_3 = basket_item
else:
    y_int = int(selected_year)
    filtered_df = data[data['Date'].dt.year == y_int]
    filtered_df_2 = monthly_summary[monthly_summary['Date'].dt.year == y_int]
    filtered_df_3 = basket_item[basket_item['Date'].dt.year == y_int]

st.write(f"### Showing data for: {selected_year}")

# --- 4. METRICS ---
col1, col2 = st.columns(2)
col1.metric("Total items sold", len(filtered_df))
col2.metric("Total items available", filtered_df['itemDescription'].nunique())

# --- 5. CHARTS ---
chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    fig1, ax1 = plt.subplots()
    filtered_df['itemDescription'].value_counts().head(5).plot(kind='bar', ax=ax1)
    ax1.set_title('Top selling items')
    plt.xticks(rotation=45)
    st.pyplot(fig1)

with chart_col2:
    fig2, ax2 = plt.subplots()
    # Use the binned column we created
    filtered_df_3['basket_bin'].value_counts().sort_index().plot(kind='bar', ax=ax2)
    ax2.set_title('Basket sizes')
    st.pyplot(fig2)

with chart_col3:
    fig3, ax3 = plt.subplots()
    # Ensure we plot Date vs total_sold
    filtered_df_2.plot(kind='line', x='Date', y='total_sold', ax=ax3)
    ax3.set_title('Sales Over Time')
    st.pyplot(fig3)