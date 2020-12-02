from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from Utility.Path import path_join
from collections import Counter
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
        subcat_counter = Counter([subcat for subcat_list in cat_idx2subcat_list for subcat in subcat_list])
        result_list = list()
        for cat_idx, cat_name in enumerate(idx2cat_name):
            for subcat_idx, subcat_name in enumerate(cat_idx2subcat_list[cat_idx]):
                if subcat_counter[subcat_name] > 1:
                    result_list.append([f'{cat_idx}-{subcat_idx}', cat_name, subcat_name, f'{cat_name}{subcat_name}'])
                else:
                    result_list.append([f'{cat_idx}-{subcat_idx}', cat_name, subcat_name, subcat_name])

        # result_list = [[f'{cat_idx}-{subcat_idx}', cat_name, subcat_name] for cat_idx, cat_name in enumerate(idx2cat_name)
        #                for subcat_idx, subcat_name in enumerate(cat_idx2subcat_list[cat_idx])]
        # for row in result_list:
        #     print(row)
        target_sheet.update(f'A2:D', result_list)

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

        self._write(idx2cat_name, cat_idx2subcat_list)

    def update_new_cat_by_list(self, cat_subcat_list):
        idx2cat_name, cat_idx2subcat_list = self._get_current_category()
        for cat_name, subcat_name in cat_subcat_list:
            try:
                target_idx = idx2cat_name.index(cat_name)
            except ValueError:
                target_idx = len(idx2cat_name)
                idx2cat_name.append(cat_name)
                cat_idx2subcat_list.append([])
            if subcat_name not in cat_idx2subcat_list[target_idx]:
                cat_idx2subcat_list[target_idx].append(subcat_name)
        self._write(idx2cat_name, cat_idx2subcat_list)


if __name__ == '__main__':
    gg = {
        'expense': {
            'category': [
                {'name': '飲食', 'sub_category': ['預設', '晚餐', '早餐', '午餐', '零食', '飲料', '酒', '宵夜']},
                {'name': '交通',
                 'sub_category': ['預設', '停車費', '腳踏車', '自己開車', '捷運公車', '悠遊卡', '火車高鐵客運', '共享機車']},
                {'name': '娛樂', 'sub_category': ['預設', '電影', '遊戲', '小說', '愛', '飛鏢']},
                {'name': '運動', 'sub_category': ['預設', '足球', '羽球', '溜冰', '衝浪', '攀岩', '潛水', '健身房', '游泳', '桌球', '恢復', '跑步']},
                {'name': '服飾', 'sub_category': ['預設', '化妝品', '正裝', '休閒', '內衣', '內褲', '襪子']},
                {'name': '購物', 'sub_category': ['預設', '3C', '電腦', '必需品', '生活品質']},
                {'name': '投資', 'sub_category': ['預設', '保險', '專業', '股票', '基金']},
                {'name': '帳單', 'sub_category': ['預設', '水費', '電費', '房租', '電話費']},
                {'name': '社交', 'sub_category': ['預設']},
                {'name': '日常', 'sub_category': ['預設', '日常用品', '剪頭髮', '隱形眼鏡', '日常服務', '營養補充']},
                {'name': '禮物', 'sub_category': ['預設', '禮金', '票券', '幫出錢']},
                {'name': '花錢消災', 'sub_category': ['預設', '打賭', '麻將', '彩券', '罰單']},
                {'name': '旅遊', 'sub_category': ['預設', '住宿', '食物', '玩樂', '交通']},
                {'name': '醫療', 'sub_category': ['預設', '生病', '牙齒', '健康檢查', '運動傷害']},
                {'name': '住宿', 'sub_category': ['預設', '家具', '消耗品', '日用品']},

            ],
            'budget': 25000,
            'items': [
                {
                    'datetime': '2016-04-05 12:07:15',
                    'amount': 120,
                    'description': '',
                    'category': 0,
                    'sub_category': 3
                },
            ]
        },
    }

    manager = CategoryManager()

    cat_subcat_list = [
        (cat['name'], sub_cat) for cat in gg['expense']['category'] for sub_cat in cat['sub_category']
    ]
    manager.update_new_cat_by_list(cat_subcat_list)

    # manager.update_new_cat('交通', '飛機')
    # manager.update_new_cat('交通', '計程車')
    # manager.update_new_cat('飲食', '土')

