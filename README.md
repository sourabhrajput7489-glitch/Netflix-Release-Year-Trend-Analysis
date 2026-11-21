# Netflix Release Year Trend Analysis — Task 4

**Medium-level Data Analysis Project | Python • Pandas • Matplotlib • Streamlit • Darsh**

## Overview
Analyze the original release years of Netflix-catalog titles, yearly title counts, movie-versus-TV-show trends, and year-over-year (YoY) growth or decline. The interactive Streamlit dashboard supports year-range and content-type filters, historical comparisons, a Darsh 3D scatter plot, insights, and CSV downloads.

## Task workflow
1. Organize content by `release_year`.
2. Calculate distinct titles released in each year.
3. Compute year-over-year growth and identify decline years.
4. Visualize release-year trends and compare Movies with TV Shows.
5. Interpret trends and report limitations.

## Features
- Sidebar: release-year range, content type, and top-N release years
- KPIs: total titles, Movies, TV Shows, peak release year
- Release-year line chart and Movies vs TV Shows comparison
- YoY growth/decline bar chart and top-year ranking table
- Content-type pie chart and Darsh 3D visualization
- Data-driven business insights and CSV downloads
- Jupyter notebook with reproducible analysis

## Dataset and interpretation
Input: `data/Cleaned_Netflix.csv`. A title is counted once per `show_id` and original `release_year` (duplicate IDs are removed). Invalid or missing years are dropped. `release_year` means the **original release year of the title**, not the year it was added to Netflix. The catalog's yearly distribution **does not measure Netflix's own production or annual additions**. The 2021 count may be incomplete depending on dataset coverage; early-year counts are small. YoY growth is undefined if the previous year's count is zero; the first year's growth is also undefined.

## Project structure
```text
Netflix-Release-Year-Trend-Analysis/
├── app.py
├── main.ipynb
├── README.md
├── requirements.txt
├── .gitignore
└── data/
    ├── Cleaned_Netflix.csv
    ├── Yearly_Content_Analysis.csv
    └── Yearly_Growth_Analysis.csv
```

## Installation (Ubuntu/Linux)
```bash
cd ~/Netflix-Release-Year-Trend-Analysis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open `http://localhost:8501` in your browser. For the notebook, open `main.ipynb` in VS Code and select the project's Python kernel; use **Run All**. Do not execute `.ipynb` with `python main.ipynb` because it is JSON, not a Python script.

**Darsh note:** The dashboard imports `darsh`. If your Darsh package is a custom/local package rather than one available from PyPI, install the exact local version you used in development. Its 3D plot depends on that implementation.

## Output files
- `data/Yearly_Content_Analysis.csv`: original release year, content type, distinct title count
- `data/Yearly_Growth_Analysis.csv`: year, title count, YoY growth percent

## Tech stack
Python, Pandas, Matplotlib, Streamlit, Plotly (Darsh 3D figure), Darsh, Jupyter.

## Author
Sourabh Singh Rajput  
GitHub: https://github.com/sourabhrajput7489-glitch/Netflix-Release-Year-Trend-Analysis
