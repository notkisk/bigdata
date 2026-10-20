# TP03: Interactive Data Analysis and Visualization with Power BI

## Deliverables

- `File.csv`: imported dataset.
- `transform.pq`: Power Query cleaning steps.
- `measures.dax`: DAX measures.
- `report.md`: six-line findings summary.
- `dashboard.svg`: final dashboard evidence mockup.

Power BI Desktop is required to save the final `.pbix` file. Open Power BI Desktop, select **Get data > Text/CSV**, choose `File.csv`, and apply the steps in `transform.pq`.

## Data preparation

The query promotes headers, sets data types, trims text, replaces missing numeric values with zero, and removes duplicate rows.

## Dashboard

Create these visuals from the cleaned table:

1. KPI cards: `Total Sales`, `Total Quantity`, and `Order Count`.
2. Bar chart: `Category` by `Total Sales`.
3. Column chart: `Region` by `Total Sales`.
4. Bar chart: `Region` by `Total Quantity`.
5. Line chart: `Date` by `Total Sales`.
6. Slicers: `Region`, `Category`, and `Date`.

Save the finished report as `TP03_PowerBI.pbix` and capture the dashboard as a screenshot. The included `dashboard.svg` shows the required layout and values.
