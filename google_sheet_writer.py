# pip install google_spreadsheet
# pip install google-auth-oauthlib
import sys
from datetime import datetime as dt
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import re


def get_log_errors():
    err_results = []
    with open(file=LOGS_PATH, mode='r', encoding='UTF-8') as file:
        for line in file.readlines():
            error_pattern = rf'{CHECK_DATE}.+ERROR.+'
            err_result = re.search(error_pattern, line.strip())
            if err_result:
                err_results.append(line.strip())
    return ';'.join(err_results)


def write_results(log_info):
    day_number = dt.strptime(CHECK_DATE, '%Y-%m-%d').day
    # Read credentials from json-file
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)

    # Log in to the Google and build service to work with API
    http_auth = credentials.authorize(httplib2.Http())
    service = build('sheets', 'v4', http=http_auth)

    # Call the Sheets API
    sheet = service.spreadsheets()
    sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"{SHEET_NAME}!A{day_number}:B{day_number + 1}",
             "majorDimension": "ROWS",
             "values": [
                 [day_number, log_info]
             ]}
        ]
    }).execute()


def main():
    log_errors = get_log_errors()
    write_results(log_info=log_errors)


if __name__ == '__main__':
    CHECK_DATE = sys.argv[1]
    LOGS_PATH = 'data/syslog.log'
    SHEET_NAME = 'Лист1'
    SPREADSHEET_ID = '1Qy1VgUYBL5lHaViC3ipEOdA8m9XsevGzzOy1BjzEUJk'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    CREDENTIALS_FILE = 'google_api_key.json'

    main()
