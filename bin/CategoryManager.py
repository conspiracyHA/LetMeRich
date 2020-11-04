from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from Utility.Path import path_join
import gspread


class CategoryManager:
    def __init__(self):
        # https://developers.google.com/identity/protocols/oauth2/scopes

        # SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(path_join('LetMeRich-52e48c199a07.json'),
                                                                            SCOPES)

        with open(path_join('google_sheet_key.txt')) as f:
            self.spread_sheet_id = f.readline()
        self.client = gspread.authorize(self.credentials)

    def _get_current_category(self):
        sheet = self.client.open_by_key(self.spread_sheet_id)
        # print(sheet.worksheets())
        target_sheet = sheet.worksheet('category_2')
        all_values = target_sheet.get_all_values()

        idx2cat_name = list()
        cat_idx2subcat_list = list()
        for row in all_values[1:]:
            cat_idx, subcat_idx = row[0].split('-')
            cat_idx, subcat_idx = int(cat_idx), int(subcat_idx)
            cat_name, subcat_name = row[1:3]
            if cat_idx == len(idx2cat_name):
                idx2cat_name.append(cat_name)
                cat_idx2subcat_list.append([subcat_name])
                continue
            cat_idx2subcat_list[cat_idx].append(subcat_name)
        print('old')
        for cat_idx, cat_name in enumerate(idx2cat_name):
            for subcat_idx, subcat_name in enumerate(cat_idx2subcat_list[cat_idx]):
                print(f'{cat_idx}-{subcat_idx}, {cat_name}, {subcat_name}')

        return idx2cat_name, cat_idx2subcat_list

    def _write(self, idx2cat_name, cat_idx2subcat_list):
        sheet = self.client.open_by_key(self.spread_sheet_id)
        # print(sheet.worksheets())
        target_sheet = sheet.worksheet('category_2')
        result_list = [[f'{cat_idx}-{subcat_idx}', cat_name, subcat_name] for cat_idx, cat_name in enumerate(idx2cat_name)
                       for subcat_idx, subcat_name in enumerate(cat_idx2subcat_list[cat_idx])]
        for row in result_list:
            print(row)
        target_sheet.update(f'A2:C', result_list)

    def update_new_cat(self, cat_name, subcat_name):
        idx2cat_name, cat_idx2subcat_list = self._get_current_category()
        try:
            target_idx = idx2cat_name.index(cat_name)
        except ValueError:
            target_idx = len(idx2cat_name)
            idx2cat_name.append(cat_name)
            cat_idx2subcat_list.append([])
        if subcat_name not in cat_idx2subcat_list[target_idx]:
            cat_idx2subcat_list[target_idx].append(subcat_name)

        print('new')
        for cat_idx, cat_name in enumerate(idx2cat_name):
            for subcat_idx, subcat_name in enumerate(cat_idx2subcat_list[cat_idx]):
                print(f'{cat_idx}-{subcat_idx}, {cat_name}, {subcat_name}')
        self._write(idx2cat_name, cat_idx2subcat_list)


if __name__ == '__main__':
    manager = CategoryManager()
    manager.update_new_cat('交通', '飛機')
    manager.update_new_cat('交通', '計程車')
    manager.update_new_cat('飲食', '土')

