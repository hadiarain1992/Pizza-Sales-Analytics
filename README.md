# Pizza Sales Analytics Project

## Project Overview
A complete Pizza Sales Analytics project built to analyze sales performance, customer ordering patterns, pizza categories, sizes, and revenue trends using MySQL, Python, REST APIs, and an interactive dashboard.

## Technologies Used
- MySQL
- Python
- Pandas
- SQLAlchemy
- FastAPI
- Streamlit
- Plotly
- REST API

## Database
**Database Name:** `pizza_sales`

**Tables:**
- orders
- order_details
- pizzas
- pizza_types

## Key Performance Indicators
- Total Revenue
- Total Orders
- Total Pizzas Sold
- Average Order Value

## Dashboard Features
- Interactive date range filter
- Pizza category filter
- Pizza size filter
- Monthly revenue analysis
- Category-wise sales analysis
- Size-wise sales analysis
- Top 5 best-selling pizzas
- Peak ordering hours

## API Endpoints
- `/kpis`
- `/filter-options`
- `/monthly-revenue`
- `/sales-by-category`
- `/sales-by-size`
- `/top-pizzas`
- `/peak-hours`

API Documentation: `http://127.0.0.1:8000/docs`

## Project Results
- Total Revenue: $817,860.05
- Total Orders: 21,350
- Total Pizzas Sold: 49,574
- Average Order Value: $38.31

## Dataset Period
January 1, 2015 – December 31, 2015

## Installation and Setup

### Prerequisites
- Python 3.10 or later
- MySQL Server
- MySQL Workbench

### 1. Set Up the Database
1. Start MySQL Server.
2. Create a database named `pizza_sales`.
3. Open and execute `sql/schema.sql` in MySQL Workbench to create the tables.
4. Import the CSV files from the `data/` folder into their corresponding tables.

Recommended import order:
- pizza_types
- pizzas
- orders
- order_details

### 2. Configure Database Credentials
1. Copy `.env.example` and rename the copy to `.env`.
2. Open `.env` and enter your own MySQL credentials.

Example:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=pizza_sales
```

Do not share your `.env` file or upload it publicly.

### 3. Install Python Dependencies

Run from the project root directory:

```bash
python -m pip install -r requirements.txt
```

### 4. Start FastAPI

Open the first terminal in the project directory:

```bash
python -m uvicorn api.main:app --reload
```

API Documentation: `http://127.0.0.1:8000/docs`

### 5. Start Streamlit Dashboard

Open a second terminal in the project directory:

```bash
python -m streamlit run dashboard/app.py
```

Dashboard: `http://localhost:8501`

Keep both terminals running while using the dashboard.

## Project Structure

- `data/` – CSV datasets
- `sql/` – Database schema and SQL analysis scripts
- `api/` – FastAPI application
- `dashboard/` – Streamlit dashboard
- `.env.example` – Sample database configuration
- `requirements.txt` – Python dependencies
- `README.md` – Project documentation

## Purpose
This project demonstrates SQL querying, relational database management, Python data analysis, REST API development, and interactive business intelligence dashboard development.