from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from Utility.Path import path_join
from collections import Counter
import gspread


class ItemManager:
    def __init__(self):
        # https://developers.google.com/identity/protocols/oauth2/scopes

        # SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(path_join('LetMeRich-52e48c199a07.json'),
                                                                            SCOPES)

        with open(path_join('google_sheet_key.txt')) as f:
            self.spread_sheet_id = f.readline()
        self.client = gspread.authorize(self.credentials)

    def override_items(self, items):
        sheet = self.client.open_by_key(self.spread_sheet_id)
        target_sheet = sheet.worksheet('items')
        target_sheet.update(f'A2:D', items)