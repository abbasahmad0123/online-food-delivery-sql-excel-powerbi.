# Online Food Delivery — SQL, Excel & Power BI

A small end-to-end analytics project for an online food delivery dataset. This repository contains database scripts / exported data, Excel analysis workbooks, and a Power BI report (.pbix) that demonstrates data modeling, transformation, and interactive visualizations for common delivery KPIs.

## Table of contents
- [Project overview](#project-overview)
- [Contents](#contents)
- [Requirements](#requirements)
- [Getting started](#getting-started)
- [Data model & metrics](#data-model--metrics)
- [Power BI report notes](#power-bi-report-notes)
- [Excel workbook notes](#excel-workbook-notes)
- [SQL scripts & database](#sql-scripts--database)
- [How to extend](#how-to-extend)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project overview
This project showcases an analytics workflow for online food delivery:
- Raw and transformed data stored / modeled with SQL
- Ad-hoc analysis and intermediate calculations in Excel
- Interactive storytelling and dashboards in Power BI

Typical use cases:
- Explore orders, customers, restaurants, and delivery performance
- Calculate KPIs such as delivery time, order volume, average order value
- Build filterable visuals to analyze top restaurants, busiest hours, and customer cohorts

## Contents
- `Online Food Delivery.pbix` — Power BI Desktop report (interactive dashboards & data model)
- `README.md` — this file
- (Optional) `sql/` — SQL scripts to create/seed the analytical database (if present)
- (Optional) `data/` — CSV or exported datasets (if present)
- (Optional) `excel/` — Excel workbook(s) with supporting analysis (if present)

> Note: The repository currently contains the Power BI `.pbix` file. If you plan to add SQL scripts or CSVs, place them in `sql/` and `data/` respectively.

## Requirements
- Power BI Desktop (or Power BI Service to publish) — to open `.pbix` and refresh the model
- A SQL engine (optional) — SQL Server, PostgreSQL, SQLite, MySQL, etc., if you want to run SQL scripts locally
- Excel (optional) — for any provided Excel analysis files
- Basic knowledge of Power Query / DAX if you want to modify the PBIX

## Getting started

1. Clone the repository:
   git clone https://github.com/abbasahmad0123/online-food-delivery-sql-excel-powerbi.

2. Open the Power BI report:
   - Install Power BI Desktop (if not installed).
   - Open `Online Food Delivery.pbix`.
   - If the report uses external data sources, update the data source settings and credentials, then click "Refresh".

3. (Optional) Run SQL scripts:
   - If `sql/` scripts are provided, run them in your SQL engine to create tables and load sample data.
   - Adjust connection strings and file paths if scripts expect CSV imports.

4. (Optional) Open Excel files:
   - Inspect formulas, pivot tables, and data tables in `excel/` (if present).

## Data model & metrics
Common tables and fields expected in this project (may vary if you add/modify data):
- Orders: order_id, customer_id, restaurant_id, order_datetime, delivery_datetime, total_amount, status
- Customers: customer_id, name, signup_date, city
- Restaurants: restaurant_id, name, cuisine, city
- Deliveries: delivery_id, order_id, driver_id, pickup_datetime, delivered_datetime
- Drivers: driver_id, name, region

Example KPIs included or suggested:
- Total orders, revenue (sum of total_amount)
- Average Order Value (AOV) = revenue / number of orders
- Average delivery time = AVG(delivery_datetime - order_datetime)
- On-time delivery rate = % deliveries within SLA
- Orders by hour, day, restaurant, and city

## Power BI report notes
- Data sources: The `.pbix` may contain an embedded data model or external queries. If queries point to local files or a database, update the data source in Power BI.
- Key pages: (example)
  - Overview / Executive summary with top-level KPIs
  - Orders & Revenue trends (time series)
  - Delivery performance & SLA analysis
  - Restaurant & customer segmentation
- Refresh: After updating data sources, use the Refresh button in Power BI Desktop to reload data.
- Customization: You can edit queries in Power Query, adjust relationships in the model view, and create or modify DAX measures.

## Excel workbook notes
- Use Excel for fast exploratory analysis, exporting pivot reports, or preparing data for import.
- If present, check for named tables and refreshable data connections.
- Consider exporting intermediate tables from Excel as CSV to use with SQL or Power BI.

## SQL scripts & database
If you decide to include SQL scripts:
- Place schema and seed scripts in `sql/` (e.g. `sql/schema.sql`, `sql/seed_data.sql`).
- Include a README inside `sql/` explaining required engine and how to run (psql, sqlcmd, sqlite3, etc.).
- Sample flow:
  1. Create database/schema: `schema.sql`
  2. Load data from CSVs: `seed_data.sql` (or use bulk load)
  3. Run transformation queries to prepare aggregates and lookup tables

## How to extend
- Add nightly refresh by deploying PBIX to Power BI Service and scheduling refresh (requires Power BI Pro / Premium).
- Add ETL automation using Python / Azure Data Factory / SQL Server Integration Services.
- Add more dimensions: promotions, payment methods, customer lifetime metrics.
- Add forecasting visuals (Power BI forecasting) to predict demand.

## Contributing
Contributions are welcome. Suggested steps:
1. Fork the repo.
2. Create a branch for your feature or fix: `git checkout -b feat/my-feature`
3. Add scripts, data, or report changes and update README if necessary.
4. Open a pull request describing the change.

## License
Include a license file (e.g., MIT) if you want others to reuse the content. Add `LICENSE` to the repo and update this section.

## Contact
Created by abbasahmad0123. For questions or help, open an issue in this repository.

---
If you want, I can:
- Customize the README with details about the specific tables/measures in your PBIX (I can inspect if you attach text exports of the model or list of datasets),
- Generate SQL schema and sample seed scripts from a small sample of your data,
- Create a short CONTRIBUTING.md and LICENSE file for the repo.
Which of these should I do next?