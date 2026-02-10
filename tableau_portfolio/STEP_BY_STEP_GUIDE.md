# Step-by-Step Guide: Building the Jakarta Hotel Dashboard

## Phase 1: Data Connection
1. Open **Tableau Public**.
2. Click **Connect** > **Text file**.
3. Select `str_reports/data/jakarta_daily_2024_2025.csv`.
4. Ensure `Date` is recognized as a Date field. If not, click the icon above the column and change to "Date".

## Phase 2: Calculated Fields
Create these fields to enable dynamic analysis:

**1. Weekend Flag**
```
IF DATEPART('weekday', [Date]) = 1 OR DATEPART('weekday', [Date]) = 7 
THEN 'Weekend' 
ELSE 'Weekday' 
END
```

**2. RevPAR Variance (YoY)**
*Note: This requires a Table Calculation in the view, usually `(ZN(SUM([Revpar])) - LOOKUP(ZN(SUM([Revpar])), -12)) / ABS(LOOKUP(ZN(SUM([Revpar])), -12))` if viewing by Month, but simple Variance is easier:*
```
[Revpar] - [Compset Revpar]
```
*(Name this "RevPAR vs CompSet")*

## Phase 3: Building the Sheets

### Sheet 1: KPI Overview (The "Ban" Numbers)
*   **Columns**: Measure Names
*   **Rows**: Measure Values
*   **Filter**: Date (Range: Latest Month or selected period)
*   **Measures to Show**: Avg `Occupancy`, Avg `ADR`, Avg `RevPAR`.
*   **Design**: Make the numbers BIG. Add comparison to CompSet in tooltips.

### Sheet 2: Monthly Trend (Line Chart)
*   **Columns**: `Date` (Right-click > drill down to **Month** continuous).
*   **Rows**: `Occupancy` and `Compset Occupancy` (Drag both to Rows, Right-click second axis > Dual Axis > Synchronize Axis).
*   **Color**: Property = Orange, CompSet = Grey.
*   **Goal**: Show where you outperform the market.

### Sheet 3: Market Share Indices (Heat Map)
*   **Columns**: `Date` (Month).
*   **Rows**: Metric Names (`MPI`, `ARI`, `RGI`).
*   **Color**: Use `Measure Values`. Set center to 100.
    *   **Red**: < 100 (Underperforming)
    *   **Green/Blue**: > 100 (Outperforming)
*   **Goal**: Instantly spot months where you lost market share.

### Sheet 4: Day of Week Analysis (Bar Chart)
*   **Columns**: `Day Of Week` (Sort: Sun, Mon, Tue...).
*   **Rows**: `RevPAR`.
*   **Color**: `Weekend Flag`.
*   **Goal**: See if weekends or weekdays drive the most revenue.

## Phase 4: Dashboard Assembly
1.  Set Size to **Fixed Size** > **Generic Desktop (1366 x 768)**.
2.  Drag **KPI Overview** to the top.
3.  Place **Monthly Trend** in the middle.
4.  Place **Market Share** and **Day of Week** at the bottom side-by-side.
5.  Search for a "Dark Mode" container structure if you want it to match your website.
6.  **Action**: Use the Monthly Trend as a filter (Dashboard > Actions > Filter) so clicking a month filters the Day of Week chart.

## Phase 5: Publishing
1.  **File > Save to Tableau Public**.
2.  Log in.
3.  Name it: "Jakarta Hotel Market Performance 2024-25".
4.  Copy the link and add it to your `project-bali.html` or `index.html`!
