from datetime import datetime
from tools.order_tools import get_order
from tools.product_tools import get_product

def evaluate_return(order_id):
    order = get_order(order_id)

    if "error" in order:
        return {
            "eligible": False,
            "reason": "Order not found"
        }

    product = get_product(order["product_id"])

    if "error" in product:
        return {
            "eligible": False,
            "reason": "Product not found"
        }

    order_date = datetime.strptime(
        order["order_date"],
        "%Y-%m-%d"
    )

    today = datetime.now()

    days_since_purchase = (
        today - order_date
    ).days

    if product["is_clearance"]:

        return {
            "eligible": False,
            "return_type": "not_allowed",
            "reason": "Clearance items are final sale",
            "policy_applied": "Clearance Policy"
        }

    if product["vendor"] == "Aurelia Couture":

        return {
            "eligible": True,
            "return_type": "exchange_only",
            "reason": "Aurelia Couture items are exchange only",
            "policy_applied": "Vendor Exception"
        }

    if product["vendor"] == "Nocturne":

        if days_since_purchase <= 21:

            return {
                "eligible": True,
                "return_type": "full_refund",
                "reason": "Nocturne items have a 21-day return window",
                "policy_applied": "Vendor Exception"
            }

        else:

            return {
                "eligible": False,
                "return_type": "not_allowed",
                "reason": "Return window exceeded for Nocturne item",
                "policy_applied": "Vendor Exception"
            }

    if product["is_sale"]:

        if days_since_purchase <= 7:

            return {
                "eligible": True,
                "return_type": "store_credit",
                "reason": "Sale items are returnable within 7 days for store credit",
                "policy_applied": "Sale Item Policy"
            }

        else:

            return {
                "eligible": False,
                "return_type": "not_allowed",
                "reason": "Sale item return window exceeded",
                "policy_applied": "Sale Item Policy"
            }


    if days_since_purchase <= 14:

        return {
            "eligible": True,
            "return_type": "full_refund",
            "reason": "Return allowed within 14 days",
            "policy_applied": "Normal Return Policy"
        }


    return {
        "eligible": False,
        "return_type": "not_allowed",
        "reason": "Return window exceeded",
        "policy_applied": "Normal Return Policy"
    }
