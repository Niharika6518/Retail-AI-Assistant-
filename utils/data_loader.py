import pandas as pd
import ast

inventory_df = pd.read_csv("data/product_inventory.csv")

inventory_df["tags"] =inventory_df["tags"].apply(
    lambda x:[tag.strip().lower() for tag in x.split(",")])

inventory_df["sizes_available"]=inventory_df["sizes_available"].apply(
    lambda x:[size.strip().lower() for size in x.split("|")]
)

inventory_df["stock_per_size"] = inventory_df["stock_per_size"].apply(
    lambda x: ast.literal_eval(x)
)

orders_df = pd.read_csv("data/orders.csv")

orders_df["order_date"]=pd.to_datetime(orders_df["order_date"])

orders_df["size"]=orders_df["size"].astype(str)

with open("data/policy.txt","r",encoding="utf-8") as file:
    policy_text=file.read()