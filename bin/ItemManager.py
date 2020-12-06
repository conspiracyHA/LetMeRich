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
        self.sheet = self.client.open_by_key(self.spread_sheet_id)
        self.target_sheet = self.sheet.worksheet('items')

    def insert_item(self, date, cat_subcat_idx_str, amount, descr):
        all_items = self.target_sheet.get_all_values()
        all_items = all_items[1:]
        all_items.append([date, cat_subcat_idx_str, amount, descr])
        self.target_sheet.update(f'A2:D', all_items)