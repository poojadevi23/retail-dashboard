import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("lulu_uae_master_2000.csv")
    df['order_date'] = pd.to_datetime(df['order_dat'], errors='coerce')
    return df

df = load_data()

st.title("📊 Retail Analytics Dashboard")

st.sidebar.header("Filters")

city = st.sidebar.multiselect("City", df["city"].dropna().unique())
channel = st.sidebar.multiselect("Channel", df["channel"].dropna().unique())
category = st.sidebar.multiselect("Category", df["category"].dropna().unique())

filtered_df = df.copy()

if city:
    filtered_df = filtered_df[filtered_df["city"].isin(city)]
if channel:
    filtered_df = filtered_df[filtered_df["channel"].isin(channel)]
if category:
    filtered_df = filtered_df[filtered_df["category"].isin(category)]

total_revenue = filtered_df["line_value"].sum()
total_orders = filtered_df["order_id"].nunique()
avg_order_value = total_revenue / total_orders if total_orders else 0

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"{total_revenue:,.2f}")
col2.metric("Orders", total_orders)
col3.metric("Avg Order Value", f"{avg_order_value:,.2f}")

st.markdown("---")
sales_trend = filtered_df.groupby("order_date")["line_value"].sum().reset_index()
fig1 = px.line(sales_trend, x="order_date", y="line_value", title="Sales Trend")
st.plotly_chart(fig1, use_container_width=True
city_sales = filtered_df.groupby("city")["line_value"].sum().reset_index()
fig2 = px.bar(city_sales, x="city", y="line_value", title="City Sales")
st.plotly_chart(fig2, use_container_width=True)
cat_sales = filtered_df.groupby("category")["line_value"].sum().reset_index()
fig3 = px.pie(cat_sales, names="category", values="line_value", title="Category Share")
st.plotly_chart(fig3, use_container_width=True)
