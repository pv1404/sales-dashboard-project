import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
)

# --- DATA LOADING AND PREPARATION ---
@st.cache_data
def load_data():
    """Loads, cleans, and prepares the sales data."""
    df = pd.read_csv('sales_data.csv')
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['Revenue'] = df['UnitsSold'] * df['SalePrice']
    df['Month'] = df['OrderDate'].dt.to_period('M').astype(str)
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
st.sidebar.markdown("Use the filters below to drill down into the data.")

# Region Filter
region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Product Filter
product = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Apply filters to the dataframe
df_selection = df.query(
    "Region == @region & Product == @product"
)

# Check if the dataframe is empty after filtering
if df_selection.empty:
    st.warning("No data available for the selected filters. Please adjust your selection.")
    st.stop() # Stop the app from running further

# --- MAIN PAGE ---
st.title("📊 Interactive Sales Performance Dashboard")
st.markdown("##") # Adds a small space

# --- KEY PERFORMANCE INDICATORS (KPIs) ---
total_revenue = int(df_selection["Revenue"].sum())
total_units_sold = int(df_selection["UnitsSold"].sum())
avg_sale_price = round(df_selection["SalePrice"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.metric(label="Total Revenue", value=f"${total_revenue:,}")
with middle_column:
    st.metric(label="Total Units Sold", value=f"{total_units_sold:,}")
with right_column:
    st.metric(label="Average Sale Price", value=f"${avg_sale_price}")

st.markdown("---")

# --- DATA VISUALIZATIONS ---

# Monthly Revenue Trend
monthly_revenue = df_selection.groupby('Month')['Revenue'].sum().reset_index()
fig_monthly_revenue = px.line(
    monthly_revenue,
    x="Month",
    y="Revenue",
    title="<b>Monthly Revenue Trend</b>",
    template="plotly_white"
)
fig_monthly_revenue.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='lightgray')
)

# Sales by Region
sales_by_region = df_selection.groupby('Region')['Revenue'].sum().sort_values(ascending=False).reset_index()
fig_sales_by_region = px.bar(
    sales_by_region,
    x="Region",
    y="Revenue",
    title="<b>Sales by Region</b>",
    template="plotly_white"
)
fig_sales_by_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Revenue ($)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

# Sales by Product
sales_by_product = df_selection.groupby('Product')['UnitsSold'].sum().sort_values(ascending=False).reset_index()
fig_sales_by_product = px.pie(
    sales_by_product,
    names="Product",
    values="UnitsSold",
    title="<b>Sales by Product</b>",
    template="plotly_white"
)
fig_sales_by_product.update_traces(textposition='inside', textinfo='percent+label')

# Display charts
st.plotly_chart(fig_monthly_revenue, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_sales_by_region, use_container_width=True)
with col2:
    st.plotly_chart(fig_sales_by_product, use_container_width=True)


# --- SALES FORECASTING ---
st.markdown("## 🔮 Sales Forecasting")
st.markdown("This section provides a simple sales forecast for the next 6 months.")

# Prepare data for forecasting
monthly_data = df.groupby('Month')['Revenue'].sum().reset_index()
monthly_data['Month_Num'] = np.arange(len(monthly_data))

# Simple Linear Regression Model
X = monthly_data[['Month_Num']]
y = monthly_data['Revenue']
model = LinearRegression()
model.fit(X, y)

# Forecast for the next 6 months
future_months_num = np.arange(len(monthly_data), len(monthly_data) + 6).reshape(-1, 1)
future_sales = model.predict(future_months_num)

# Create future month labels
last_month = pd.to_datetime(monthly_data['Month'].iloc[-1]).to_period('M')
future_month_labels = [(last_month + i).strftime('%Y-%m') for i in range(1, 7)]

# Combine historical and forecasted data for plotting
forecast_df = pd.DataFrame({'Month': future_month_labels, 'Forecasted Revenue': future_sales})
historical_df = monthly_data[['Month', 'Revenue']].rename(columns={'Revenue': 'Historical Revenue'})
combined_df = pd.concat([historical_df.tail(12), forecast_df], ignore_index=True)


# Plotting the forecast
fig_forecast = px.line(
    combined_df,
    x='Month',
    y=['Historical Revenue', 'Forecasted Revenue'],
    title="<b>Sales Forecast vs. Historical Data (Last 12 Months)</b>",
    template="plotly_white"
)
fig_forecast.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    legend_title="Legend",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_forecast, use_container_width=True)

# --- ACTIONABLE INSIGHTS ---
st.markdown("## 💡 Key Business Insight")
top_region = sales_by_region.iloc[0]
st.info(
    f"""
    **Top Performing Region:** The **{top_region['Region']}** region is the top-performing market, contributing **${int(top_region['Revenue']):,}** in revenue.
    This suggests that strategic initiatives and marketing budgets could be focused on replicating the success of this region in other markets, or further investing here to maximize growth.
    """
)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
