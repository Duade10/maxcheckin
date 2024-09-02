import io
import json
import time

import gspread
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError
from openpyxl import Workbook
from openpyxl.styles import Font
from utils import data_processing


# Function to get Google Sheets client
def get_google_sheet_client(json_key):
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_info(
        json_key,
        scopes=scopes
    )
    return gspread.authorize(credentials)


# Function to retry fetching a worksheet
def get_worksheet_with_retry(client, sheet_id, sheet_name, max_retries=5, delay=1):
    for attempt in range(max_retries):
        try:
            sheet = client.open_by_key(key=sheet_id)
            worksheet = sheet.worksheet(sheet_name)
            return worksheet
        except APIError as e:
            if e.response.status_code == 429:
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
                else:
                    raise
            else:
                raise


# Function to add ordinal suffix to a day
def add_ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = 'TH'
    else:
        suffix = {1: 'ST', 2: 'ND', 3: 'RD'}.get(n % 10, 'TH')
    return f"{n}{suffix}"


# Function to find the maximum and minimum values and their indices
def get_max_and_min_index(values):
    flattened_data = [float(item[0]) for item in values]
    max_value = max(flattened_data)
    min_value = min(flattened_data)
    max_index = flattened_data.index(max_value)
    min_index = flattened_data.index(min_value)
    return max_value, max_index, min_value, min_index


# Function to analyze worksheet data
def analyze_worksheet(worksheet, column):
    values = worksheet.get_values(f"{column}8:{column}31")
    max_value, max_index, min_value, min_index = get_max_and_min_index(values)
    return {
        "Max Load": max_value,
        "Max Hour": f"{max_index + 1}00",
        "Min Load": min_value,
        "Min Hour": f"{min_index + 1}00"
    }


# Function to create Excel file with the analysis results
def create_excel_file(results):
    wb = Workbook()
    ws = wb.active
    ws.title = "Analysis Results"

    headers = ["Date", "Transformer", "Max Load", "Max Hour", "Min Load", "Min Hour"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for day_result in results:
        for transformer in ["4T2", "4T1", "4T6"]:
            row = [
                day_result["Date"],
                transformer,
                day_result[transformer]["Max Load"],
                day_result[transformer]["Max Hour"],
                day_result[transformer]["Min Load"],
                day_result[transformer]["Min Hour"]
            ]
            ws.append(row)

    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    return excel_file


# Main function to run the Streamlit app
def main():
    st.title("Google Sheets Data Analysis")

    # Load the JSON key directly from the "keys.json" file
    with open("keys.json") as file:
        json_key = json.load(file)

    sheet_id = st.text_input("Enter the Google Sheet ID")
    sheet_id = data_processing.extract_google_sheet_id(sheet_id)
    start_day = st.number_input("Start Day", min_value=1, max_value=31, value=1)
    end_day = st.number_input("End Day", min_value=start_day, max_value=31, value=31)

    if st.button("Analyze Data"):
        try:
            client = get_google_sheet_client(json_key)

            results = []
            progress_bar = st.progress(0)

            for i, day in enumerate(range(start_day, end_day + 1)):
                sheet_name = add_ordinal(day)
                worksheet = get_worksheet_with_retry(client, sheet_id, sheet_name)

                day_results = {
                    "Date": f"August {day}, 2024",
                    "4T2": analyze_worksheet(worksheet, "B"),
                    "4T1": analyze_worksheet(worksheet, "C"),
                    "4T6": analyze_worksheet(worksheet, "D")
                }
                results.append(day_results)

                progress = (i + 1) / (end_day - start_day + 1)
                progress_bar.progress(progress)

                time.sleep(5)  # Add a delay between requests

            for day_result in results:
                st.subheader(day_result["Date"])
                for transformer in ["4T2", "4T1", "4T6"]:
                    st.write(f"{transformer}:")
                    st.write(
                        f"Max Load: {day_result[transformer]['Max Load']} at {day_result[transformer]['Max Hour']}")
                    st.write(
                        f"Min Load: {day_result[transformer]['Min Load']} at {day_result[transformer]['Min Hour']}")
                st.write("---")

            for transformer in ["4T2", "4T1", "4T6"]:
                df = pd.DataFrame([
                    {
                        "Date": result["Date"],
                        "Max Load": result[transformer]["Max Load"],
                        "Min Load": result[transformer]["Min Load"]
                    } for result in results
                ])

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df["Date"], y=df["Max Load"], mode='lines+markers', name='Max Load'))
                fig.add_trace(go.Scatter(x=df["Date"], y=df["Min Load"], mode='lines+markers', name='Min Load'))
                fig.update_layout(title=f"{transformer} Load Over Time", xaxis_title="Date", yaxis_title="Load")
                st.plotly_chart(fig)

            # Create and offer Excel file for download
            excel_file = create_excel_file(results)
            st.download_button(
                label="Download Excel file",
                data=excel_file,
                file_name="analysis_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# Run the main function if this is the main module
if __name__ == "__main__":
    main()
