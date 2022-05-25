from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from Utility.Path import path_join
from collections import Counter
from gspread.exceptions import WorksheetNotFound
import gspread


DEFAULT_CAT = [
    ['cat-subcat', 'cat_name', 'subcat_name', 'unique_name'],
    ['0-0', '飲食', '預設', '飲食預設'],
    ['0-1', '飲食', '晚餐', '晚餐'],
    ['0-2', '飲食', '早餐', '早餐'],
    ['0-3', '飲食', '午餐', '午餐'],
    ['0-4', '飲食', '零食', '零食'],
    ['0-5', '飲食', '飲料', '飲料'],
    ['0-6', '飲食', '酒', '酒'],
    ['0-7', '飲食', '宵夜', '宵夜'],
    ['1-0', '交通', '預設', '交通預設'],
    ['1-1', '交通', '停車費', '停車費'],
    ['1-2', '交通', '腳踏車', '腳踏車'],
    ['1-3', '交通', '自己開車', '自己開車'],
    ['1-4', '交通', '捷運公車', '捷運公車'],
    ['1-5', '交通', '悠遊卡', '悠遊卡'],
    ['1-6', '交通', '火車高鐵客運', '火車高鐵客運'],
    ['1-7', '交通', '共享機車', '共享機車'],
    ['2-0', '娛樂', '預設', '娛樂預設'],
    ['2-1', '娛樂', '電影', '電影'],
    ['2-2', '娛樂', '遊戲', '遊戲'],
    ['2-3', '娛樂', '小說', '小說'],
    ['2-4', '娛樂', '愛', '愛'],
    ['2-5', '娛樂', '飛鏢', '飛鏢'],
    ['3-0', '運動', '預設', '運動預設'],
    ['3-1', '運動', '足球', '足球'],
    ['3-2', '運動', '羽球', '羽球'],
    ['3-3', '運動', '溜冰', '溜冰'],
    ['3-4', '運動', '衝浪', '衝浪'],
    ['3-5', '運動', '攀岩', '攀岩'],
    ['3-6', '運動', '潛水', '潛水'],
    ['3-7', '運動', '健身房', '健身房'],
    ['3-8', '運動', '游泳', '游泳'],
    ['3-9', '運動', '桌球', '桌球'],
    ['3-10', '運動', '恢復', '恢復'],
    ['3-11', '運動', '跑步', '跑步'],
    ['4-0', '服飾', '預設', '服飾預設'],
    ['4-1', '服飾', '化妝品', '化妝品'],
    ['4-2', '服飾', '正裝', '正裝'],
    ['4-3', '服飾', '休閒', '休閒'],
    ['4-4', '服飾', '內衣', '內衣'],
    ['4-5', '服飾', '內褲', '內褲'],
    ['4-6', '服飾', '襪子', '襪子'],
    ['5-0', '購物', '預設', '購物預設'],
    ['5-1', '購物', '3C', '3C'],
    ['5-2', '購物', '電腦', '電腦'],
    ['5-3', '購物', '必需品', '必需品'],
    ['5-4', '購物', '生活品質', '生活品質'],
    ['6-0', '投資', '預設', '投資預設'],
    ['6-1', '投資', '保險', '保險'],
    ['6-2', '投資', '專業', '專業'],
    ['6-3', '投資', '股票', '股票'],
    ['6-4', '投資', '基金', '基金'],
    ['7-0', '帳單', '預設', '帳單預設'],
    ['7-1', '帳單', '水費', '水費'],
    ['7-2', '帳單', '電費', '電費'],
    ['7-3', '帳單', '房租', '房租'],
    ['7-4', '帳單', '電話費', '電話費'],
    ['8-0', '社交', '預設', '社交預設'],
    ['9-0', '日常', '預設', '日常預設'],
    ['9-1', '日常', '日常用品', '日常用品'],
    ['9-2', '日常', '剪頭髮', '剪頭髮'],
    ['9-3', '日常', '隱形眼鏡', '隱形眼鏡'],
    ['9-4', '日常', '日常服務', '日常服務'],
    ['9-5', '日常', '營養補充', '營養補充'],
    ['10-0', '禮物', '預設', '禮物預設'],
    ['10-1', '禮物', '禮金', '禮金'],
    ['10-2', '禮物', '票券', '票券'],
    ['10-3', '禮物', '幫出錢', '幫出錢'],
    ['11-0', '花錢消災', '預設', '花錢消災預設'],
    ['11-1', '花錢消災', '打賭', '打賭'],
    ['11-2', '花錢消災', '麻將', '麻將'],
    ['11-3', '花錢消災', '彩券', '彩券'],
    ['11-4', '花錢消災', '罰單', '罰單'],
    ['12-0', '旅遊', '預設', '旅遊預設'],
    ['12-1', '旅遊', '住宿', '住宿'],
    ['12-2', '旅遊', '食物', '食物'],
    ['12-3', '旅遊', '玩樂', '玩樂'],
    ['12-4', '旅遊', '交通', '交通'],
    ['13-0', '醫療', '預設', '醫療預設'],
    ['13-1', '醫療', '生病', '生病'],
    ['13-2', '醫療', '牙齒', '牙齒'],
    ['13-3', '醫療', '健康檢查', '健康檢查'],
    ['13-4', '醫療', '運動傷害', '運動傷害'],
    ['14-0', '住宿', '預設', '住宿預設'],
    ['14-1', '住宿', '家具', '家具'],
    ['14-2', '住宿', '消耗品', '消耗品'],
    ['14-3', '住宿', '日用品', '日用品'],
]


class UserManager:
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
        self.target_sheet = self.sheet.worksheet('Users')

    def _get_all_users(self):
        users = self.target_sheet.get_all_values()
        # print(users)
        return users[1:]

    def create_user_worksheet(self, user_id):
        try:
            self.sheet.worksheet(f'{user_id}_items')
        except WorksheetNotFound:
            self.sheet.add_worksheet(title=f'{user_id}_items', rows="2", cols="4")
            target_sheet = self.sheet.worksheet(f'{user_id}_items')
            target_sheet.update(f'A1:D', [['datetime', 'category', 'amount', 'description']])

        try:
            self.sheet.worksheet(f'{user_id}_category')
        except WorksheetNotFound:
            self.sheet.add_worksheet(title=f'{user_id}_category', rows="2", cols="4")
            target_sheet = self.sheet.worksheet(f'{user_id}_category')
            # target_sheet.append_rows([DEFAULT_CAT])
            target_sheet.update(f'A1:D', DEFAULT_CAT)

    def add_user(self, chat_object):
        all_users = self._get_all_users()
        new_user = [
            str(getattr(chat_object, attr, '')) for attr in
            ['id', 'first_name', 'last_name', 'user_name', 'type']
        ]
        if new_user[0] in [x[0] for x in all_users]:
            return
        else:
            all_users.append(new_user)
        self.target_sheet.update(f'A2:E', all_users)

    def get_user_worksheet(self, user_id):
        try:
            return {
                'item_sheet': self.sheet.worksheet(f'{user_id}_items'),
                'cat_sheet': self.sheet.worksheet(f'{user_id}_category'),
            }
        except WorksheetNotFound:
            return None

