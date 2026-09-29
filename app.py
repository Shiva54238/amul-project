import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Amul Analytics Dashboard", page_icon="🥛", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "amul_analytics_sample.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["profit"] = df["revenue"] * df["profit_margin"]
    df["marketing_efficiency"] = df["marketing_spend"] / df["revenue"]
    return df


def sidebar_filters(df):
    regions = sorted(df["region"].unique())
    categories = sorted(df["product_category"].unique())

    st.sidebar.header("Filters")
    selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
    selected_categories = st.sidebar.multiselect(
        "Product Category", categories, default=categories
    )

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    start_date, end_date = st.sidebar.date_input(
        "Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

    filtered = df[
        (df["region"].isin(selected_regions))
        & (df["product_category"].isin(selected_categories))
        & (df["date"].dt.date >= start_date)
        & (df["date"].dt.date <= end_date)
    ]
    return filtered


def show_kpis(df):
    total_revenue = df["revenue"].sum()
    total_units = df["units_sold"].sum()
    total_profit = df["profit"].sum()
    avg_margin = (df["profit_margin"].mean() * 100)

    kpi_cols = st.columns(4)
    kpi_cols[0].metric("Revenue", f"₹{total_revenue:,.0f}")
    kpi_cols[1].metric("Units Sold", f"{total_units:,.0f}")
    kpi_cols[2].metric("Profit", f"₹{total_profit:,.0f}")
    kpi_cols[3].metric("Avg Margin", f"{avg_margin:.1f}%")


def charts(df):
    monthly = (
        df.groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"), units_sold=("units_sold", "sum"))
        .sort_values("month")
    )

    regional = (
        df.groupby("region", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
        .sort_values("revenue", ascending=False)
    )

    category = (
        df.groupby("product_category", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
        .sort_values("revenue", ascending=False)
    )

    scatter_df = df.groupby("product_name", as_index=False).agg(
        revenue=("revenue", "sum"),
        marketing_spend=("marketing_spend", "sum"),
        profit=("profit", "sum"),
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Monthly Revenue Trend")
        revenue_chart = px.line(
            monthly,
            x="month",
            y="revenue",
            markers=True,
            title="Revenue by Month",
            color_discrete_sequence=["#FF6B35"],
        )
        st.plotly_chart(revenue_chart, use_container_width=True)

    with right:
        st.subheader("Units Sold Trend")
        units_chart = px.bar(
            monthly,
            x="month",
            y="units_sold",
            title="Units Sold by Month",
            color_discrete_sequence=["#1F77B4"],
        )
        st.plotly_chart(units_chart, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Regional Revenue Performance")
        region_chart = px.bar(
            regional,
            x="region",
            y="revenue",
            color="region",
            title="Revenue by Region",
        )
        st.plotly_chart(region_chart, use_container_width=True)

    with right:
        st.subheader("Product Category Revenue")
        category_chart = px.pie(
            category,
            names="product_category",
            values="revenue",
            title="Revenue Share by Category",
        )
        st.plotly_chart(category_chart, use_container_width=True)

    st.subheader("Profit vs Marketing Spend")
    scatter_chart = px.scatter(
        scatter_df,
        x="marketing_spend",
        y="profit",
        size="revenue",
        hover_name="product_name",
        title="Return Efficiency by Product",
        color="profit",
        color_continuous_scale="Viridis",
    )
    st.plotly_chart(scatter_chart, use_container_width=True)


def main():
    df = load_data()
    filtered = sidebar_filters(df)

    st.title("Amul Company Analytics Dashboard")
    st.caption("Advanced business intelligence overview using sample sales and performance data")

    if filtered.empty:
        st.warning("No data matches the selected filters.")
        return

    show_kpis(filtered)
    st.markdown("---")
    charts(filtered)

    with st.expander("Raw Data Preview"):
        st.dataframe(filtered.head(50), use_container_width=True)


if __name__ == "__main__":
    main()
