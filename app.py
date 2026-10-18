import streamlit as st
from report import load_data, DATA_FILE

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("Superstore Sales Dashboard")

df = load_data(DATA_FILE)

# ---------- Filters ----------
st.sidebar.header("Filters")

all_regions = sorted(df["Region"].unique())
all_categories = sorted(df["Category"].unique())

regions = st.sidebar.multiselect("Region", all_regions, default=all_regions)
categories = st.sidebar.multiselect("Category", all_categories, default=all_categories)

df = df[df["Region"].isin(regions) & df["Category"].isin(categories)]

if df.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# ---------- KPIs ----------
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = total_profit / total_sales * 100
orders_count = df["Order ID"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")
col4.metric("Orders", f"{orders_count:,}")

st.divider()

# ---------- Charts ----------
left, right = st.columns(2)

with left:
    st.subheader("Monthly Sales")
    monthly = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
    monthly.index = monthly.index.to_timestamp()
    st.line_chart(monthly)

with right:
    st.subheader("Profit by Sub-Category")
    sub_profit = df.groupby("Sub-Category")["Profit"].sum().sort_values()
    st.bar_chart(sub_profit)

st.divider()

st.subheader("Profit by Discount Level")
discount_profit = df.groupby("Discount")["Profit"].sum()
discount_profit.index = [f"{round(d * 100)}%" for d in discount_profit.index]
st.bar_chart(discount_profit)
