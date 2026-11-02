
from datetime import date
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Pizza Sales Analytics API",
    description="Filtered Pizza Sales Business Intelligence API",
    version="2.0.0"
)

DB_USER = "root"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_NAME = "pizza_sales"

connection_url = URL.create(
    "mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)

engine = create_engine(connection_url)


def get_filters(start_date, end_date, category, size):
    conditions = []
    params = {}

    if start_date:
        conditions.append("o.order_date >= :start_date")
        params["start_date"] = start_date

    if end_date:
        conditions.append("o.order_date <= :end_date")
        params["end_date"] = end_date

    if category:
        conditions.append("pt.category = :category")
        params["category"] = category

    if size:
        conditions.append("p.pizza_size = :size")
        params["size"] = size

    where = ""
    if conditions:
        where = " AND " + " AND ".join(conditions)

    return where, params


def fetch_data(query, params):
    with engine.connect() as connection:
        return connection.execute(
            text(query), params
        ).mappings().all()


@app.get("/")
def home():
    return {"message": "Pizza Sales API is running!"}


@app.get("/filter-options")
def filter_options():
    query = """
        SELECT
            (SELECT MIN(order_date) FROM orders) AS min_date,
            (SELECT MAX(order_date) FROM orders) AS max_date
    """

    with engine.connect() as connection:
        dates = connection.execute(text(query)).mappings().first()

        categories = connection.execute(text(
            "SELECT DISTINCT category FROM pizza_types ORDER BY category"
        )).scalars().all()

        sizes = connection.execute(text(
            "SELECT DISTINCT pizza_size FROM pizzas ORDER BY pizza_size"
        )).scalars().all()

    return {
        "min_date": str(dates["min_date"]),
        "max_date": str(dates["max_date"]),
        "categories": categories,
        "sizes": sizes
    }


@app.get("/kpis")
def get_kpis(
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    size: str = None
):
    where, params = get_filters(
        start_date, end_date, category, size
    )

    query = """
        SELECT
            SUM(od.quantity * p.price) AS total_revenue,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(od.quantity) AS total_pizzas_sold
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
        WHERE 1=1
    """ + where

    rows = fetch_data(query, params)
    result = rows[0]

    revenue = float(result["total_revenue"] or 0)
    orders = int(result["total_orders"] or 0)

    return {
        "total_revenue": revenue,
        "total_orders": orders,
        "total_pizzas_sold": int(result["total_pizzas_sold"] or 0),
        "average_order_value": round(revenue / orders, 2) if orders else 0
    }


@app.get("/monthly-revenue")
def monthly_revenue(
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    size: str = None
):
    where, params = get_filters(start_date, end_date, category, size)

    query = """
        SELECT
            MONTH(o.order_date) AS month_number,
            MONTHNAME(o.order_date) AS month,
            ROUND(SUM(od.quantity * p.price), 2) AS revenue
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
        WHERE 1=1
    """ + where + """
        GROUP BY MONTH(o.order_date), MONTHNAME(o.order_date)
        ORDER BY month_number
    """

    return [dict(row) for row in fetch_data(query, params)]


@app.get("/sales-by-category")
def sales_by_category(
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    size: str = None
):
    where, params = get_filters(start_date, end_date, category, size)

    query = """
        SELECT
            pt.category,
            SUM(od.quantity) AS pizzas_sold
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
        WHERE 1=1
    """ + where + """
        GROUP BY pt.category
        ORDER BY pizzas_sold DESC
    """

    return [dict(row) for row in fetch_data(query, params)]


@app.get("/sales-by-size")
def sales_by_size(
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    size: str = None
):
    where, params = get_filters(start_date, end_date, category, size)

    query = """
        SELECT
            p.pizza_size AS size,
            SUM(od.quantity) AS pizzas_sold
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
        WHERE 1=1
    """ + where + """
        GROUP BY p.pizza_size
        ORDER BY pizzas_sold DESC
    """

    return [dict(row) for row in fetch_data(query, params)]


@app.get("/top-pizzas")
def top_pizzas(
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    size: str = None
):
    where, params = get_filters(start_date, end_date, category, size)

    query = """
        SELECT
            pt.name AS pizza_name,
            SUM(od.quantity) AS pizzas_sold
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
        WHERE 1=1
    """ + where + """
        GROUP BY pt.name
        ORDER BY pizzas_sold DESC
        LIMIT 5
    """

    return [dict(row) for row in fetch_data(query, params)]


@app.get("/peak-hours")
def peak_hours(
    start_date: date = None,
    end_date: date = None,
    category: str = None,
    size: str = None
):
    where, params = get_filters(start_date, end_date, category, size)

    query = """
        SELECT
            HOUR(o.order_time) AS hour,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        JOIN pizza_types pt ON p.pizza_type_id = pt.pizza_type_id
        WHERE 1=1
    """ + where + """
        GROUP BY HOUR(o.order_time)
        ORDER BY hour
    """

    return [dict(row) for row in fetch_data(query, params)]
