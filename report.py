import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_FILE = "clean_superstore.csv"


def load_data(path):
    return pd.read_csv(path, parse_dates=["Order Date", "Ship Date"])


def show_kpis(df):
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    print("Total Sales:", round(total_sales, 2))
    print("Total Profit:", round(total_profit, 2))
    print("Profit Margin %:", round(total_profit / total_sales * 100, 2))
    print("Number of Orders:", df["Order ID"].nunique())


def summary_by(df, column):
    summary = df.groupby(column)[["Sales", "Profit"]].sum()
    summary["Profit Margin %"] = summary["Profit"] / summary["Sales"] * 100
    return summary.sort_values("Sales", ascending=False)


def discount_by(df, column):
    return (df.groupby(column)["Discount"].mean() * 100).sort_values(ascending=False)


def sales_by_month_number(df):
    return df.groupby(df["Order Date"].dt.month)["Sales"].sum()


def central_vs_other(df, sub_categories):
    subset = df[df["Sub-Category"].isin(sub_categories)].copy()
    subset["Is Central"] = subset["Region"] == "Central"
    result = subset.groupby(["Sub-Category", "Is Central"])["Discount"].mean().unstack() * 100
    result.columns = ["Other Regions", "Central"]
    return result


def plot_monthly_trend(df):
    monthly = df.groupby(df["Order Date"].dt.to_period("M"))["Sales"].sum()
    monthly.index = monthly.index.to_timestamp()
    plt.figure(figsize=(10, 5))
    plt.plot(monthly.index, monthly.values)
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.savefig("monthly_sales_trend.png")
    plt.show()


def find_outliers(df, column):
    q1, q3 = np.percentile(df[column], [25, 75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df[column] < lower) | (df[column] > upper)]
    return outliers, lower, upper


def main():
    df = load_data(DATA_FILE)

    show_kpis(df)

    print("\nPerformance by Category:")
    print(summary_by(df, "Category").round(2))

    print("\nPerformance by Region:")
    print(summary_by(df, "Region").round(2))

    print("\nAverage Discount by Region (%):")
    print(discount_by(df, "Region").round(1))

    print("\nTotal Sales by Calendar Month:")
    print(sales_by_month_number(df).round(2))

    print("\nAverage Discount (%): Central vs Other Regions")
    problem_subs = ["Furnishings", "Tables", "Appliances", "Bookcases", "Machines"]
    print(central_vs_other(df, problem_subs).round(1))
    outliers, lower, upper = find_outliers(df, "Profit")
    print("\nProfit Outliers:")
    print("Normal range:", round(lower, 2), "to", round(upper, 2))
    print("Number of outliers:", len(outliers))
    print("Share of all rows (%):", round(len(outliers) / len(df) * 100, 1))

    big_wins = outliers[outliers["Profit"] > upper]
    big_losses = outliers[outliers["Profit"] < lower]
    print("Unusually high profits:", len(big_wins), "rows, total", round(big_wins["Profit"].sum(), 2))
    print("Unusually large losses:", len(big_losses), "rows, total", round(big_losses["Profit"].sum(), 2))

    print("Avg discount, big losses (%):", round(big_losses["Discount"].mean() * 100, 1))
    print("Avg discount, all other rows (%):", round(df.drop(big_losses.index)["Discount"].mean() * 100, 1))
    print("Big losses with discount >= 30% (%):", round((big_losses["Discount"] >= 0.3).mean() * 100, 1))

    plot_monthly_trend(df)


if __name__ == "__main__":
    main()