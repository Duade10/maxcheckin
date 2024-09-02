import streamlit as st
import io
import openpyxl
import pandas as pd
from datetime import datetime

from utils import google_sheets, data_processing


def main():
    st.title("Google Sheet Data Processor")

    sheet_id = st.text_input("Enter Google Sheet ID")
    sheet_id = data_processing.extract_google_sheet_id(sheet_id)
    worksheet = st.text_input("Enter Worksheet Name")

    if st.button("Process Sheet"):
        if sheet_id and worksheet:
            process_sheet(sheet_id, worksheet)
        else:
            st.error("Please enter both Sheet ID and Worksheet Name")


def process_sheet(sheet_id, worksheet):
    # Get worksheet data
    worksheet = google_sheets.get_worksheet(sheet_id, worksheet)
    list_of_lists = worksheet.get_all_values()
    filtered_data = list(filter(lambda x: any(x), list_of_lists))

    headers = [
        'sub_region', 'substations', 'lines', 'voltage_level',
        'relay_tripping_indication', 'cause_of_outage', 'open_date',
        'open_time', 'close_date', 'close_time', 'outage_duration',
        'last_load', 'energy_loss', 'remarks'
    ]

    # Create workbook and worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.append(headers)

    # Group data by 'lines' column
    grouped_data = {}
    for row in filtered_data:
        if str(row[12]).lower() == "forced":
            try:
                line = row[4]
                if line not in grouped_data:
                    grouped_data[line] = []
                grouped_data[line].append(row)
            except IndexError:
                continue

    for line_group in grouped_data.values():
        for row in line_group:
            if 'CB F' != row[14]:
                try:
                    sub_region = data_processing.format_subregion_name(row[2])
                    substations = data_processing.format_substation_name(row[3])
                    lines = data_processing.format_line_name(row[4])
                    voltage_level = 33
                    relay_tripping_indication = data_processing.get_correct_fault(row[14])
                    cause_of_outage = 'Line Fault'
                    open_date = row[5]
                    open_time = data_processing.join_time(row[6], row[7])
                    close_date = row[8]
                    close_time = data_processing.join_time(row[9], row[10])
                    outage_duration = round(
                        calculate_time_difference(open_date, open_time, close_date, close_time), 2)
                    last_load = float(row[13])
                    energy_loss = round(outage_duration * last_load, 2)
                    remarks = str(row[19]).upper()
                    single_row = [sub_region, substations, lines, voltage_level, relay_tripping_indication,
                                  cause_of_outage, open_date, open_time, close_date, close_time, outage_duration,
                                  last_load, energy_loss, remarks]
                    worksheet.append(single_row)
                except IndexError:
                    continue

    # Save workbook to BytesIO object
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)

    # Create a download button
    st.download_button(
        label="Download Excel file",
        data=output,
        file_name="output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Display preview of the data
    df = pd.DataFrame(worksheet.values)
    df.columns = df.iloc[0]
    df = df[1:]
    st.write(df)


def calculate_time_difference(start_date_str, start_time_str, end_date_str, end_time_str):
    start_datetime = datetime.strptime(start_date_str + ' ' + start_time_str, '%d/%m/%Y %H:%M')
    end_datetime = datetime.strptime(end_date_str + ' ' + end_time_str, '%d/%m/%Y %H:%M')
    time_difference = (end_datetime - start_datetime).total_seconds() / 3600
    return time_difference


if __name__ == "__main__":
    main()
