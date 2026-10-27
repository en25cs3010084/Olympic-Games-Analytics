# Global Olympic Sports Performance Analysis

## Project contents
- `app.py`: interactive Streamlit dashboard with filters, bar charts, medal composition, trends and CSV export.
- `data/country_medals.csv`: selected-country medal sample for 2008, 2012, 2016, 2020 and 2024.
- `data/sport_events_demo.csv`: sport programme demonstration dataset.
- `data/year_summary.csv`: summary calculated from the selected-country sample.
- `Olympic_Project_Data.xlsx`: workbook with all data sheets.
- `Project_Report.docx`: editable project report.

## Run the dashboard
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.
5. Open the local address shown in the terminal.

## Important data limitation
This is a working academic prototype. The country file contains selected leading delegations only, not every National Olympic Committee. Sport event counts are explicitly demonstration estimates and should not be represented as a verified official dataset. Before formal submission, replace/validate these with official IOC/Olympics data and cite the exact dataset URL and access date. The dashboard itself will work with the included CSV column structure.

## Suggested presentation flow
1. State the objective and dataset limitations.
2. Select years/countries using the sidebar.
3. Compare medal totals and medal composition.
4. Explain trends without claiming causation.
5. Show sport event comparison as a demonstration.
6. Export filtered data to CSV.
