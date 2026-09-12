# Data Storytelling — Online Retail

## Internship Task 2

A decision-oriented analytical report built from the UCI Online Retail transaction dataset. The project extends the earlier EDA work into a structured data story: **data quality → business metrics → patterns → decisions → actions**.

### Dataset
- UCI Machine Learning Repository — Online Retail
- License: CC BY 4.0
- DOI: 10.24432/C5CG6D
- Official page: https://archive.ics.uci.edu/dataset/502/online%2Bretail
- Place the legally sourced Excel file at `data/online_retail_II.xlsx`.

### Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python src/data_storytelling.py
```

### Outputs
- `outputs/charts/` — individual analytical charts
- `outputs/final_eda_dashboard.png` — consolidated dashboard
- `outputs/cleaned_online_retail.csv` — cleaned analytical dataset
- `outputs/analysis_summary.txt` — generated metrics
- `docs/Data_Storytelling_Report.pdf` — internship report
- `screenshots/` — submission screenshots

### Key verified findings from the completed Task 1 analysis
- Original dataset: 541,909 rows and 8 columns.
- 5,268 duplicate rows were removed.
- Final analytical dataset: 392,692 rows and 14 columns.
- Missing values after cleaning: 0.
- Total revenue: £8,887,208.89.
- Quantity sold: 5,152,002.
- Orders: 18,532.
- Customers: 4,338.
- Products: 3,665.
- Average order value: £479.56.
- Quantity–Revenue correlation: approximately 0.91.
- UnitPrice–Revenue correlation: approximately 0.08.
- UK is the dominant revenue-generating country.
- November 2011 is the highest-revenue month in the analyzed period.
- PAPER CRAFT, LITTLE BIRDIE is the highest-revenue product.

### Data quality and limitations
The analysis removes duplicates, incomplete customer/product records, and non-positive quantity/price rows for sales-performance analysis. This means cancellations/returns and incomplete customer records are not represented in the final sales-performance view. Correlation is descriptive and does not establish causation.

### Resources used
- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- OpenPyXL
- ReportLab
- UCI Online Retail dataset
- Pandas documentation
- Matplotlib documentation
- Kaggle Learn

No passwords, API keys, tokens, private credentials, or sensitive personal information are included.

### GitHub
Existing Task 1 repository:
https://github.com/rahulraj2007k-pixel/EDA-Dashboard
