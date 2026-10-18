import pandas as pd

df = pd.read_csv("Sample - Superstore.csv", encoding="latin-1")
print(df.head())
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")


text_cols = df.select_dtypes(include="object").columns

for col in text_cols:
    df[col] = df[col].str.strip()

df.to_csv("clean_superstore.csv", index=False)
print("Saved successfully")