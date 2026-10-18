import pandas as pd



# Load the cleaned data
df = pd.read_csv("clean_superstore.csv", parse_dates=["Order Date", "Ship Date"])

# Calculate key metrics (KPIs)
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
profit_margin = total_profit / total_sales * 100
orders_count = df["Order ID"].nunique()

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Profit Margin %:", round(profit_margin, 2))
print("Number of Orders:", orders_count)

# Sales and profit by category
category_summary = df.groupby("Category")[["Sales", "Profit"]].sum()
category_summary = category_summary.sort_values("Sales", ascending=False)

print("\nSales and Profit by Category:")
print(category_summary.round(2))

# Profit by sub-category (to find what hurts the profit)
subcategory_profit = df.groupby("Sub-Category")["Profit"].sum()
subcategory_profit = subcategory_profit.sort_values()

print("\nProfit by Sub-Category (lowest to highest):")
print(subcategory_profit.round(2))

# Average discount by sub-category
avg_discount = df.groupby("Sub-Category")["Discount"].mean()
avg_discount = avg_discount.sort_values(ascending=False)

print("\nAverage Discount by Sub-Category:")
print((avg_discount * 100).round(1))

# Tables: profit at each discount level
tables = df[df["Sub-Category"] == "Tables"]
tables_by_discount = tables.groupby("Discount")["Profit"].agg(["sum", "count"])

print("\nTables - Profit by Discount Level:")
print(tables_by_discount.round(2))

import matplotlib.pyplot as plt

# Chart: Tables profit by discount level
plt.figure(figsize=(8, 5))
plt.bar(tables_by_discount.index.astype(str), tables_by_discount["sum"])
plt.title("Tables: Profit by Discount Level")
plt.xlabel("Discount")
plt.ylabel("Total Profit")
plt.axhline(0, color="black", linewidth=0.8)
plt.savefig("tables_profit_by_discount.png")
plt.show()

# Monthly sales trend
df["Month"] = df["Order Date"].dt.to_period("M")
monthly_sales = df.groupby("Month")["Sales"].sum()
monthly_sales.index = monthly_sales.index.to_timestamp()

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index, monthly_sales.values)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.savefig("monthly_sales_trend.png")
plt.show()

# Seasonality: total sales by calendar month
df["Month Number"] = df["Order Date"].dt.month
seasonality = df.groupby("Month Number")["Sales"].sum()

print("\nTotal Sales by Calendar Month:")
print(seasonality.round(2))

# Sales and profit by region
region_summary = df.groupby("Region")[["Sales", "Profit"]].sum()
region_summary["Profit Margin %"] = region_summary["Profit"] / region_summary["Sales"] * 100
region_summary = region_summary.sort_values("Sales", ascending=False)

print("\nPerformance by Region:")
print(region_summary.round(2))

# Average discount by region
region_discount = df.groupby("Region")["Discount"].mean() * 100

print("\nAverage Discount by Region (%):")
print(region_discount.sort_values(ascending=False).round(1))

# Central region: profit by sub-category
central = df[df["Region"] == "Central"]
central_profit = central.groupby("Sub-Category")["Profit"].sum().sort_values()

print("\nCentral Region - Lowest 5 Sub-Categories by Profit:")
print(central_profit.head(5).round(2))

# Compare discounts: Central vs other regions for the problem sub-categories
problem_subs = ["Furnishings", "Tables", "Appliances", "Bookcases", "Machines"]
subset = df[df["Sub-Category"].isin(problem_subs)].copy()
subset["Is Central"] = subset["Region"] == "Central"

comparison = subset.groupby(["Sub-Category", "Is Central"])["Discount"].mean().unstack() * 100
comparison.columns = ["Other Regions", "Central"]

print("\nAverage Discount (%): Central vs Other Regions")
print(comparison.round(1))

# Compare discounts: Central vs other regions for the problem sub-categories
problem_subs = ["Furnishings", "Tables", "Appliances", "Bookcases", "Machines"]
subset = df[df["Sub-Category"].isin(problem_subs)].copy()
subset["Is Central"] = subset["Region"] == "Central"

comparison = subset.groupby(["Sub-Category", "Is Central"])["Discount"].mean().unstack() * 100
comparison.columns = ["Other Regions", "Central"]

print("\nAverage Discount (%): Central vs Other Regions")
print(comparison.round(1))

# Compare discounts: Central vs other regions for the problem sub-categories
problem_subs = ["Furnishings", "Tables", "Appliances", "Bookcases", "Machines"]
subset = df[df["Sub-Category"].isin(problem_subs)].copy()
subset["Is Central"] = subset["Region"] == "Central"

comparison = subset.groupby(["Sub-Category", "Is Central"])["Discount"].mean().unstack() * 100
comparison.columns = ["Other Regions", "Central"]

print("\nAverage Discount (%): Central vs Other Regions")
print(comparison.round(1))

# Chart: discount comparison, Central vs other regions
comparison.plot(kind="bar", figsize=(9, 5))
plt.title("Average Discount: Central vs Other Regions")
plt.xlabel("Sub-Category")
plt.ylabel("Average Discount (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("central_discount_comparison.png")
plt.show()