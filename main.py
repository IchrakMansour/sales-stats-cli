import argparse
import json
from stats import (
    load_orders, 
    count_orders,
    total_revenue, 
    average_order, 
    top_products, 
    revenue_by_category, 
    revenue_by_month, 
    best_customer 
)

def main() :
    parser = argparse.ArgumentParser(description="Sales Statistics CLI")

    parser.add_argument("file", help="Path to the orders CSV file")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--out", default="report.json")

    args = parser.parse_args()

    try:
        orders = load_orders(args.file)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return
    except ValueError as error:
        print(f"Error: {error}")
        return
    
    number_of_orders = count_orders(orders)
    revenue = total_revenue(orders)
    average = average_order(orders)
    products = top_products(orders, args.top)
    categories = revenue_by_category(orders)
    months = revenue_by_month(orders)
    customer,  best_customer_spent = best_customer(orders)

    print(f"Orders: {number_of_orders}")
    print(f"Revenue: {revenue:.2f}") # Print the first order for inspection
    print(f"Average order value: {average:.2f}")
    print(f"Top {args.top} products")

    for product, amount in products:
        print(f"  {product}: {amount:.2f}")

    print("Revenue per category:")
    for category, amount in categories.items():
        print(f"  {category}: {amount:.2f}")

    print("Revenue by month:")
    for month, amount in months.items():
        print(f"  {month}: {amount:.2f}")

    if customer is not None:
        print(f"Best customer: {customer} ({ best_customer_spent:.2f})")
    else:
        print("Best customer: None")

    report = {
        "total_orders": number_of_orders,
        "total_revenue": revenue,
        "average_order_value": average,
        "top_products": [
            {"product": product, "revenue": amount}
            for product, amount in products
        ],
        "revenue_by_category": categories,
        "revenue_by_month": months,
        "best_customer": {
            "name": customer,
            "total_spent": amount
        } if customer is not None else None
    }


    with open(args.out, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(f"Report will be saved to {args.out}")

if __name__ == "__main__":
    main()
