import csv
from collections import defaultdict
from datetime import datetime

def load_orders(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        required_columns = {
            "order_id", 
            "date",
            "customer", 
            "product", 
            "category", 
            "quantity", 
            "unit_price"
        }

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no header")

        missing_columns = required_columns - set(reader.fieldnames)
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

        orders = list(reader)
        
    for order in orders:
        try:
            quantity = int(order["quantity"])
            price = float(order["unit_price"])
        except (ValueError, TypeError):  
            raise ValueError(f"Invalid quantity or unit_price in order: {order.get('order_id')}")

        if quantity <= 0 :
            raise ValueError( f"Quantity must be positive in order {order.get('order_id')}")

        if price < 0 :
            raise  ValueError(f"Price cannot be negative in order {order.get('order_id')}")
    return orders

def count_orders(orders):
    order_ids = set()

    for order in orders:
        order_ids.add(order["order_id"])
    return len(order_ids)

def total_revenue(orders):
    total = 0

    for order in orders:
        quantity = int(order["quantity"])
        price = float(order["unit_price"])
        total += quantity * price

    return total

def average_order(orders):
    number_of_orders = count_orders(orders)

    if not number_of_orders:
        return 0

    total = total_revenue(orders)
    return total / number_of_orders

def top_products(orders, n=5):
    revenue_by_product = defaultdict(float)

    for order in orders:
        product = order["product"]
        quantity = int(order["quantity"])
        price = float(order["unit_price"])
        revenue_by_product[product] += quantity * price

    sorted_products = sorted(revenue_by_product.items(), key=lambda x: x[1], reverse=True)
    return sorted_products[:n]  

def revenue_by_category(orders):
    revenue_by_category = defaultdict(float)

    for order in orders:
        category = order["category"]
        quantity = int(order["quantity"])
        price = float(order["unit_price"])
        revenue_by_category[category] += quantity * price

    return dict(revenue_by_category)

def revenue_by_month(orders):
    revenue_by_month = defaultdict(float)

    for order in orders:
        order_date = datetime.strptime(order["date"], "%Y-%m-%d")
        month = order_date.strftime("%Y-%m")
        quantity = int(order["quantity"])
        price = float(order["unit_price"])
        revenue_by_month[month] += quantity * price

    return dict(sorted(revenue_by_month.items()))

def best_customer(orders):
    revenue_by_customer = defaultdict(float)

    for order in orders:
        customer = order["customer"]
        quantity = int(order["quantity"])
        price = float(order["unit_price"])
        revenue_by_customer[customer] += quantity * price

    if not revenue_by_customer:
        return None, 0

    best_customer = max(revenue_by_customer, key=revenue_by_customer.get)
    return best_customer, revenue_by_customer[best_customer]