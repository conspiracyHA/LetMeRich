from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from Utility.Path import path_join

# https://github.com/googleapis/google-api-python-client/blob/master/docs/start.md

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDENTIAL_FILE = path_join('LetMeRich-52e48c199a07.json')

with open(path_join('google_sheet_key.txt')) as f:
    SAMPLE_SPREADSHEET_ID = f.readline()

SAMPLE_RANGE_NAME = 'category_2!A2:C'


def main():

    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_FILE, SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    # https://googleapis.github.io/google-api-python-client/docs/dyn/sheets_v4.html
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row)


if __name__ == '__main__':
    main()