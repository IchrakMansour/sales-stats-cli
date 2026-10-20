import pytest
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


def test_count_orders():
    orders = [
        {"order_id": "1001"},
        {"order_id": "1001"},
        {"order_id": "1002"},
    ]

    assert count_orders(orders) == 2


def sample_orders():
    return [
        {
            "order_id": "1001",
            "date": "2026-01-14",
            "customer": "Sara",
            "product": "Scarf",
            "category": "Accessories",
            "quantity": "2",
            "unit_price": "10.0",
        },
        {
            "order_id": "1001",
            "date": "2026-01-14",
            "customer": "Sara",
            "product": "Bag",
            "category": "Accessories",
            "quantity": "1",
            "unit_price": "30.0",
        },
        {
            "order_id": "1002",
            "date": "2026-02-03",
            "customer": "Ali",
            "product": "T-shirt",
            "category": "Clothing",
            "quantity": "3",
            "unit_price": "20.0",
        },
    ]


def test_total_revenue():
    assert total_revenue(sample_orders()) == 110.0


def test_average_order_value():
    assert average_order(sample_orders()) == 55.0


def test_top_products():
    result = top_products(sample_orders(), 2)

    assert result == [
        ("T-shirt", 60.0),
        ("Bag", 30.0),
    ]


def test_revenue_by_category():
    result = revenue_by_category(sample_orders())

    assert result == {
        "Accessories": 50.0,
        "Clothing": 60.0,
    }


def test_revenue_by_month():
    result = revenue_by_month(sample_orders())

    assert result == {
        "2026-01": 50.0,
        "2026-02": 60.0,
    }


def test_best_customer():
    name, amount = best_customer(sample_orders())

    assert name == "Ali"
    assert amount == 60.0


def test_empty_orders():
    assert count_orders([]) == 0
    assert total_revenue([]) == 0
    assert average_order([]) == 0
    assert top_products([], 5) == []
    assert revenue_by_category([]) == {}
    assert revenue_by_month([]) == {}
    assert best_customer([]) == (None, 0)

def test_invalid_quantity(tmp_path):
    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "order_id,date,customer,product,category,quantity,unit_price\n"
        "1001,2026-01-14,Sara,Scarf,Accessories,invalid,10.0\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Invalid quantity"):
        load_orders(str(csv_file))

def test_invalid_price(tmp_path):
    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "order_id,date,customer,product,category,quantity,unit_price\n"
        "1001,2026-01-14,Sara,Scarf,Accessories,2,invalid\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Invalid quantity"):
        load_orders(str(csv_file))

def test_zero_quantity(tmp_path):
    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "order_id,date,customer,product,category,quantity,unit_price\n"
        "1001,2026-01-14,Sara,Scarf,Accessories,0,10.0\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Quantity must be positive"):
        load_orders(str(csv_file))

def test_zero_price(tmp_path):
    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "order_id,date,customer,product,category,quantity,unit_price\n"
        "1001,2026-01-14,Sara,Scarf,Accessories,2,-10.0\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Price cannot be negative"):
        load_orders(str(csv_file))

def test_missing_column(tmp_path):
    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "order_id,date,customer,product,quantity,unit_price\n"
        "1001,2026-01-14,Sara,Scarf,2,35.0\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        load_orders(csv_file)