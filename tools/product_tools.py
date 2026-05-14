from utils.data_loader import inventory_df

def search_products(filters):

    filtered_df = inventory_df.copy()

    if "max_price" in filters:
        filtered_df = filtered_df[
            filtered_df["price"] <= filters["max_price"]
        ]

    if "tags" in filters:

        requested_tags = [
            tag.lower() for tag in filters["tags"]
        ]

        filtered_df = filtered_df[
    filtered_df["tags"].apply(
        lambda product_tags:
        any(
            requested_tag in product_tag
            or
            product_tag in requested_tag
            for requested_tag in requested_tags
            for product_tag in product_tags
        )
    )
]
    if "size" in filters:

        requested_size = str(filters["size"])

        filtered_df = filtered_df[
            filtered_df.apply(
                lambda row:
                (
                    requested_size in row["sizes_available"]
                    and
                    row["stock_per_size"].get(requested_size, 0) > 0
                ),
                axis=1
            )
        ]

    if "is_sale" in filters:

        filtered_df = filtered_df[
            filtered_df["is_sale"] == filters["is_sale"]
        ]

    if filtered_df.empty:
     return []

    filtered_df = filtered_df.sort_values(
        by="bestseller_score",
        ascending=False
    )

    results = []

    for _, row in filtered_df.iterrows():

        product_data = {
    "product_id": str(row["product_id"]),
    "title": str(row["title"]),
    "vendor": str(row["vendor"]),
    "price": int(row["price"]),
    "compare_at_price": int(row["compare_at_price"]),
    "tags": list(row["tags"]),
    "is_sale": bool(row["is_sale"]),
    "is_clearance": bool(row["is_clearance"]),
    "bestseller_score": int(row["bestseller_score"])
}

        results.append(product_data)

    return results

def get_product(product_id):
 
    product = inventory_df[
        inventory_df["product_id"] == product_id
    ]

    if product.empty:
        return {
            "error": "Product not found"
        }

    row = product.iloc[0]

    return {
    "product_id": str(row["product_id"]),
    "title": str(row["title"]),
    "vendor": str(row["vendor"]),
    "price": int(row["price"]),
    "compare_at_price": int(row["compare_at_price"]),
    "tags": list(row["tags"]),
    "sizes_available": list(row["sizes_available"]),
    "stock_per_size": dict(row["stock_per_size"]),
    "is_sale": bool(row["is_sale"]),
    "is_clearance": bool(row["is_clearance"]),
    "bestseller_score": int(row["bestseller_score"])
}