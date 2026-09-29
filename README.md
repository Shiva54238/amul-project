# Amul Analytics Dashboard

A modern Python analytics dashboard for the Amul company, built with Streamlit and Plotly. This project provides insights into sales performance, product performance, region-wise distribution, and business trends using sample data.

## Features

- Executive KPI overview
- Monthly revenue and unit sales trends
- Regional performance comparison
- Product category analysis
- Profit vs marketing efficiency insights
- Interactive filters by region and product category
- Clean, production-ready dashboard layout

## Tech Stack

- Python 3.11+
- Streamlit
- Pandas
- Plotly
- NumPy

## Project Structure

```text
amul-project/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── data/
│   └── amul_analytics_sample.csv
└── .streamlit/
    └── config.toml
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Shiva54238/amul-project.git
cd amul-project
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the dashboard:

```bash
streamlit run app.py
```

## Sample Data

The dashboard uses a sample dataset located at:

```text
data/amul_analytics_sample.csv
```

This includes records for regions, products, sales units, revenue, profit margin, and marketing spend across several months.

## Dashboard Highlights

- Total revenue overview
- Total units sold
- Average profit margin
- Cost-to-revenue efficiency
- Monthly sales performance by region
- Top-selling product categories

## Notes

This project is meant to serve as a strong starter dashboard for Amul business analytics and can be extended with real production data, ERP exports, or database integration.
