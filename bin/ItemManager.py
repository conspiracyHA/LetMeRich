from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from Utility.Path import path_join
from collections import Counter
import gspread
from gspread.exceptions import WorksheetNotFound


class ItemManager:
    def __init__(self, worksheet):
        self.worksheet = worksheet

    def insert_item(self, date, cat_subcat_idx_str, amount, descr):
        self.worksheet.append_row([date, cat_subcat_idx_str, amount, descr])

    def get_all_items(self):
        all_items = self.worksheet.get_all_values()
        all_items = all_items[1:]
        return all_items
