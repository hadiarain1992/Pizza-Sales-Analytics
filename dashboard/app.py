
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Pizza Sales Analytics",
    page_icon="🍕",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
.stApp {
    background-color: #f7f8fc;
}
h1 {
    color: #b22222;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)


def get_data(endpoint, params=None):
    response = requests.get(
        f"{API_URL}/{endpoint}",
        params=params,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


st.title("🍕 Pizza Sales Analytics Dashboard")
st.caption("Business Intelligence | MySQL | Python | FastAPI | Streamlit")
st.divider()

try:
    # Load filter options
    options = get_data("filter-options")

    min_date = pd.to_datetime(options["min_date"]).date()
    max_date = pd.to_datetime(options["max_date"]).date()

    # Sidebar filters
    st.sidebar.title("Dashboard Filters")
    st.sidebar.caption("Customize your sales analysis")

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = selected_dates[0]
        end_date = selected_dates[0]

    selected_category = st.sidebar.selectbox(
        "Pizza Category",
        ["All Categories"] + options["categories"]
    )

    selected_size = st.sidebar.selectbox(
        "Pizza Size",
        ["All Sizes"] + options["sizes"]
    )

    st.sidebar.divider()
    st.sidebar.caption("Pizza Sales Analytics | 2015")

    # Prepare API parameters
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }

    if selected_category != "All Categories":
        params["category"] = selected_category

    if selected_size != "All Sizes":
        params["size"] = selected_size

    # Fetch filtered data
    kpis = get_data("kpis", params)
    monthly = pd.DataFrame(get_data("monthly-revenue", params))
    categories = pd.DataFrame(get_data("sales-by-category", params))
    sizes = pd.DataFrame(get_data("sales-by-size", params))
    top_pizzas = pd.DataFrame(get_data("top-pizzas", params))
    hours = pd.DataFrame(get_data("peak-hours", params))

    # Business Overview
    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"${kpis['total_revenue']:,.2f}"
    )

    col2.metric(
        "Total Orders",
        f"{kpis['total_orders']:,}"
    )

    col3.metric(
        "Pizzas Sold",
        f"{kpis['total_pizzas_sold']:,}"
    )

    col4.metric(
        "Average Order Value",
        f"${kpis['average_order_value']:,.2f}"
    )

    st.caption(
        f"Showing data from {start_date} to {end_date}"
        f" | Category: {selected_category}"
        f" | Size: {selected_size}"
    )

    st.divider()

    # Monthly Revenue
    st.subheader("Monthly Revenue Analysis")

    if not monthly.empty:
        fig_monthly = px.bar(
            monthly,
            x="month",
            y="revenue",
            text_auto=".2s",
            title="Revenue by Month",
            labels={
                "month": "Month",
                "revenue": "Revenue ($)"
            }
        )
        fig_monthly.update_layout(template="plotly_white")
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.info("No monthly revenue data for selected filters.")

    st.divider()

    # Category and Size Analysis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sales by Pizza Category")

        if not categories.empty:
            fig_category = px.pie(
                categories,
                names="category",
                values="pizzas_sold",
                hole=0.45,
                title="Category Contribution"
            )
            fig_category.update_layout(template="plotly_white")
            st.plotly_chart(fig_category, use_container_width=True)
        else:
            st.info("No category data available.")

    with col2:
        st.subheader("Sales by Pizza Size")

        if not sizes.empty:
            fig_size = px.bar(
                sizes,
                x="size",
                y="pizzas_sold",
                text_auto=True,
                title="Pizza Size Performance",
                labels={
                    "size": "Pizza Size",
                    "pizzas_sold": "Pizzas Sold"
                }
            )
            fig_size.update_layout(template="plotly_white")
            st.plotly_chart(fig_size, use_container_width=True)
        else:
            st.info("No size data available.")

    st.divider()

    # Top Pizzas and Peak Hours
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 5 Bestselling Pizzas")

        if not top_pizzas.empty:
            fig_top = px.bar(
                top_pizzas.sort_values("pizzas_sold"),
                x="pizzas_sold",
                y="pizza_name",
                orientation="h",
                text_auto=True,
                title="Top Performing Pizzas",
                labels={
                    "pizza_name": "Pizza",
                    "pizzas_sold": "Quantity Sold"
                }
            )
            fig_top.update_layout(template="plotly_white")
            st.plotly_chart(fig_top, use_container_width=True)
        else:
            st.info("No bestselling pizza data available.")

    with col2:
        st.subheader("Orders by Hour")

        if not hours.empty:
            fig_hours = px.line(
                hours.sort_values("hour"),
                x="hour",
                y="total_orders",
                markers=True,
                title="Hourly Order Trend",
                labels={
                    "hour": "Hour of Day",
                    "total_orders": "Total Orders"
                }
            )
            fig_hours.update_layout(template="plotly_white")
            st.plotly_chart(fig_hours, use_container_width=True)
        else:
            st.info("No hourly order data available.")

    # Detailed data
    st.divider()
    st.subheader("Detailed Sales Data")

    with st.expander("View Monthly Revenue"):
        st.dataframe(monthly, use_container_width=True)

    with st.expander("View Category Sales"):
        st.dataframe(categories, use_container_width=True)

    with st.expander("View Pizza Size Sales"):
        st.dataframe(sizes, use_container_width=True)

    with st.expander("View Top Pizzas"):
        st.dataframe(top_pizzas, use_container_width=True)

    with st.expander("View Peak Ordering Hours"):
        st.dataframe(hours, use_container_width=True)

    st.divider()
    st.caption(
        "Pizza Sales Analytics Project | "
        "Powered by MySQL, FastAPI, Python and Streamlit"
    )

except requests.exceptions.ConnectionError:
    st.error("API connection failed. Please start the FastAPI server.")

except requests.exceptions.RequestException as error:
    st.error(f"API Error: {error}")

except Exception as error:
    st.error(f"Dashboard Error: {error}")
