import gspread
from google.oauth2.service_account import Credentials


def get_google_sheet_client():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        '../keys.json',
        scopes=scopes
    )

    return gspread.authorize(credentials)


def get_worksheet(sheet_id, worksheet_name):
    client = get_google_sheet_client()
    sheet = client.open_by_key(key=sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet
