# E-Commerce Sales & Customer Insights Dashboard

## Project Overview

This project analyzes e-commerce sales, customer behavior, products,
geography, reviews, and delivery performance using the Olist dataset.

## Objectives

1. Combine order, customer, product, and location data.
2. Clean duplicates, missing values, cancellations, and inconsistent categories.
3. Calculate business KPIs.
4. Analyze monthly trends and customer cohorts.
5. Segment customers based on purchasing behavior.
6. Identify top products, underperforming categories, high-value customers,
   and regional patterns.
7. Build an interactive Streamlit dashboard.
8. Provide data-backed recommendations.

## Key KPIs

- Total Revenue: R$ 13,591,643.70
- Total Orders: 99,441
- Average Order Value: R$ 136.68
- Unique Customers: 96,096
- Repeat Customers: 2,997
- Repeat Customer Rate: 3.12%
- On-Time Delivery Rate: 92.32%
- Late Delivery Rate: 7.68%
- Positive Review Rate: 77.07%
- Negative Review Rate: 14.69%

## Data Cleaning

The project checks duplicate records, missing values, dates, product
information, review information, and geolocation records.

Cancelled and unavailable orders were separated from completed-sales
analysis. The dataset does not provide a dedicated refund amount, so
actual refund values were not estimated.

## Analysis

The project includes:

- Monthly revenue trends
- Customer segmentation
- Customer cohort analysis
- Top products
- Top categories
- Underperforming categories
- High-value customers
- Regional revenue analysis
- Delivery performance
- Customer review analysis

## Margin

True profit margin could not be calculated because product cost/COGS
is not available in the dataset.

## Dashboard

The Streamlit dashboard includes:

- KPI cards
- Monthly revenue
- Category performance
- State performance
- Customer segmentation
- Product performance
- Dashboard filters
- Business recommendations

## Tools

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit
- Git
- GitHub
- Google Colab

## Business Recommendations

1. Investigate ways to increase repeat purchases.
2. Investigate late deliveries by state, seller, and category.
3. Analyze negative reviews alongside delivery and product performance.
4. Monitor lower-revenue categories.
5. Monitor regional revenue concentration.
6. Obtain product cost/COGS data before calculating true profit margin.

## Project Structure

dashboard/
dashboard_data/
olist_data/
README.md

## Conclusion

The project provides a data-driven view of e-commerce sales,
customers, products, geography, reviews, and delivery performance
through an interactive dashboard.
