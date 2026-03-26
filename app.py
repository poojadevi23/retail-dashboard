import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Retail Dashboard", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("lulu_uae_master_2000.csv")
    df.columns = df.columns.str.strip().str.lower()
    df['order_date'] = pd.to_datetime(df['order_datetime'], errors='coerce')
    return df

df = load_data()

st.title("Retail Analytics Dashboard")

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

total_revenue = filtered_df["line_value_aed"].sum()
total_orders = filtered_df["order_id"].nunique()
avg_order_value = total_revenue / total_orders if total_orders else 0

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"{total_revenue:,.2f}")
col2.metric("Orders", total_orders)
col3.metric("Avg Order Value", f"{avg_order_value:,.2f}")

st.markdown("---")

sales_trend = filtered_df.groupby("order_date")["line_value_aed"].sum().reset_index()
fig1 = px.line(sales_trend, x="order_date", y="line_value_aed", title="Sales Trend")
st.plotly_chart(fig1, use_container_width=True)

city_sales = filtered_df.groupby("city")["line_value_aed"].sum().reset_index()
fig2 = px.bar(city_sales, x="city", y="line_value_aed", title="City Sales")
st.plotly_chart(fig2, use_container_width=True)

cat_sales = filtered_df.groupby("category")["line_value_aed"].sum().reset_index()
fig3 = px.pie(cat_sales, names="category", values="line_value_aed", title="Category Share")
st.plotly_chart(fig3, use_container_width=True)

hour_sales = filtered_df.groupby("hour_of_day")["line_value_aed"].sum().reset_index()
fig4 = px.bar(hour_sales, x="hour_of_day", y="line_value_aed", title="Sales by Hour")
st.plotly_chart(fig4, use_container_width=True)

pay = filtered_df.groupby("payment_method")["line_value_aed"].sum().reset_index()
fig5 = px.pie(pay, names="payment_method", values="line_value_aed", title="Payment Split")
st.plotly_chart(fig5, use_container_width=True)

device = filtered_df.groupby("device_type")["line_value_aed"].sum().reset_index()
fig6 = px.bar(device, x="device_type", y="line_value_aed", title="Revenue by Device")
st.plotly_chart(fig6, use_container_width=True)

loyal = filtered_df.groupby("loyalty_member")["line_value_aed"].sum().reset_index()
fig7 = px.bar(loyal, x="loyalty_member", y="line_value_aed", title="Loyalty vs Revenue")
st.plotly_chart(fig7, use_container_width=True)
