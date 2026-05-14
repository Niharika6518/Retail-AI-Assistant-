from utils.data_loader import orders_df

def get_order(order_id):
    order = orders_df[
        orders_df["order_id"] == order_id
    ]

    if order.empty:
     return {
        "error": "Order not found"
    }
    
    row=order.iloc[0]

    return{
        "order_id": row["order_id"],
        "order_date": str(row["order_date"].date()),
        "product_id": row["product_id"],
        "size": row["size"],
        "price_paid": int(row["price_paid"]),
        "customer_id": row["customer_id"]
    }

