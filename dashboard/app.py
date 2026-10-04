
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from io import BytesIO

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="E-Commerce Sales & Customer Insights",
    page_icon="🛒",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "dashboard_data"


def show_chart(fig):
    buffer = BytesIO()
    fig.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        dpi=150
    )
    buffer.seek(0)
    st.image(buffer)
    plt.close(fig)


# =========================================================
# LOAD MAIN DATA
# =========================================================

dashboard_main = pd.read_csv(
    DATA_DIR / "dashboard_main.csv"
)

dashboard_main["order_purchase_timestamp"] = pd.to_datetime(
    dashboard_main["order_purchase_timestamp"],
    errors="coerce"
)

dashboard_main["price"] = pd.to_numeric(
    dashboard_main["price"],
    errors="coerce"
).fillna(0)

dashboard_main["freight_value"] = pd.to_numeric(
    dashboard_main["freight_value"],
    errors="coerce"
).fillna(0)

dashboard_main["year"] = (
    dashboard_main["order_purchase_timestamp"].dt.year
)

dashboard_main["month"] = (
    dashboard_main["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)

# =========================================================
# TITLE
# =========================================================

st.title("🛒 E-Commerce Sales & Customer Insights Dashboard")

st.write(
    "Sales, customer behavior, product, geographic, "
    "review and delivery analysis."
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

# Year
years = sorted(
    dashboard_main["year"]
    .dropna()
    .astype(int)
    .unique()
)

selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + years
)

# State
states = sorted(
    dashboard_main["customer_state"]
    .dropna()
    .astype(str)
    .unique()
)

selected_state = st.sidebar.selectbox(
    "State",
    ["All"] + states
)

# Category
categories = sorted(
    dashboard_main["product_category_name"]
    .dropna()
    .astype(str)
    .unique()
)

selected_category = st.sidebar.selectbox(
    "Product Category",
    ["All"] + categories
)

# Order status
statuses = sorted(
    dashboard_main["order_status"]
    .dropna()
    .astype(str)
    .unique()
)

selected_status = st.sidebar.selectbox(
    "Order Status",
    ["All"] + statuses
)

# Customer segment
customer_order_counts = (
    dashboard_main
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

repeat_customer_ids = set(
    customer_order_counts[
        customer_order_counts > 1
    ].index
)

dashboard_main["customer_segment"] = (
    dashboard_main["customer_unique_id"]
    .apply(
        lambda x:
        "Repeat Customer"
        if x in repeat_customer_ids
        else "One-time Customer"
    )
)

segments = [
    "All",
    "One-time Customer",
    "Repeat Customer"
]

selected_segment = st.sidebar.selectbox(
    "Customer Segment",
    segments
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered = dashboard_main.copy()

if selected_year != "All":
    filtered = filtered[
        filtered["year"] == selected_year
    ]

if selected_state != "All":
    filtered = filtered[
        filtered["customer_state"] == selected_state
    ]

if selected_category != "All":
    filtered = filtered[
        filtered["product_category_name"] == selected_category
    ]

if selected_status != "All":
    filtered = filtered[
        filtered["order_status"] == selected_status
    ]

if selected_segment != "All":
    filtered = filtered[
        filtered["customer_segment"] == selected_segment
    ]

# =========================================================
# FILTER SUMMARY
# =========================================================

st.sidebar.divider()

st.sidebar.write(
    f"Filtered rows: **{len(filtered):,}**"
)

# =========================================================
# KPIs
# =========================================================

st.subheader("📊 Key Performance Indicators")

total_revenue = filtered["price"].sum()

total_orders = filtered["order_id"].nunique()

total_customers = filtered[
    "customer_unique_id"
].nunique()

if total_orders > 0:
    average_order_value = (
        total_revenue / total_orders
    )
else:
    average_order_value = 0

customer_order_counts_filtered = (
    filtered
    .groupby("customer_unique_id")["order_id"]
    .nunique()
)

repeat_customers = (
    customer_order_counts_filtered > 1
).sum()

if total_customers > 0:
    repeat_rate = (
        repeat_customers / total_customers
    ) * 100
else:
    repeat_rate = 0

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "💰 Revenue",
        f"R$ {total_revenue:,.2f}"
    )

with c2:
    st.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )

with c3:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "📦 Average Order Value",
        f"R$ {average_order_value:,.2f}"
    )

with c5:
    st.metric(
        "🔁 Repeat Customer Rate",
        f"{repeat_rate:.2f}%"
    )

with c6:
    st.metric(
        "📦 Items",
        f"{len(filtered):,}"
    )

st.divider()

# =========================================================
# MONTHLY REVENUE
# =========================================================

st.subheader("📈 Monthly Revenue Trend")

monthly = (
    filtered
    .groupby("month")["price"]
    .sum()
    .reset_index()
)

if len(monthly) > 0:

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        monthly["month"],
        monthly["price"],
        marker="o"
    )

    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (R$)")
    ax.set_title("Monthly Revenue")

    plt.xticks(rotation=45)
    plt.tight_layout()

    show_chart(fig)

else:
    st.info("No data available for the selected filters.")

# =========================================================
# CATEGORY + STATE
# =========================================================

col1, col2 = st.columns(2)

# CATEGORY
with col1:

    st.subheader("🛍️ Product Categories")

    category_data = (
        filtered
        .groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    if len(category_data) > 0:

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.barh(
            category_data.index,
            category_data.values
        )

        ax.set_xlabel("Revenue (R$)")
        ax.set_title("Top Categories")

        plt.tight_layout()

        show_chart(fig)

    else:
        st.info("No category data available.")

# STATE
with col2:

    st.subheader("🗺️ Revenue by State")

    state_data = (
        filtered
        .groupby("customer_state")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    if len(state_data) > 0:

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.barh(
            state_data.index,
            state_data.values
        )

        ax.set_xlabel("Revenue (R$)")
        ax.set_title("Top States")

        plt.tight_layout()

        show_chart(fig)

    else:
        st.info("No state data available.")

# =========================================================
# CUSTOMER SEGMENTATION
# =========================================================

st.subheader("👥 Customer Segmentation")

segment_data = (
    filtered
    .groupby("customer_segment")[
        "customer_unique_id"
    ]
    .nunique()
)

if len(segment_data) > 0:

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.pie(
        segment_data.values,
        labels=segment_data.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Customer Segments")

    plt.tight_layout()

    show_chart(fig)

# =========================================================
# TOP PRODUCTS
# =========================================================

st.subheader("🏆 Top Products")

product_data = (
    filtered
    .groupby("product_id")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

if len(product_data) > 0:

    product_table = pd.DataFrame({
        "Product ID": product_data.index,
        "Revenue": product_data.values
    })

    product_table["Revenue"] = product_table[
        "Revenue"
    ].map(lambda x: f"R$ {x:,.2f}")

    st.markdown(
        product_table.to_markdown(index=False)
    )

# =========================================================
# RECOMMENDATIONS
# =========================================================

st.divider()

st.subheader("💡 Data-Backed Recommendations")

st.markdown(
    """
**1. Customer retention:** Monitor repeat-customer behavior
and investigate opportunities to increase repeat purchases.

**2. Delivery performance:** Investigate late deliveries by
state, seller and category.

**3. Product performance:** Monitor high-revenue products
while investigating lower-revenue categories.

**4. Customer experience:** Analyze negative reviews together
with delivery performance and product categories.

**5. Regional performance:** Monitor revenue concentration
across states and identify opportunities in lower-performing
regions.

**6. Margin:** True profit margin is not calculated because
the dataset does not contain product cost/COGS data.
"""
)

st.success("🎉 Dashboard loaded successfully!")
