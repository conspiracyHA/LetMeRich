from bin.Utility.Path import path_join
import json


back_path = path_join('Ahorro.json')
backup = json.load(open(back_path, 'r', encoding='utf-8'))

category_id2category = {
    '26': '健康',
    '11': '購物',
    '3': '晚餐',
    '2': '午餐',
    '1': '早餐',
    '5': '零食',
    '6': '交通',
    '17': '投資',
    '4': '飲料',
    '13': '禮物',
    '14': '禮金',
    '16': '電話費',
    '30': '旅遊',
    '7': '日常',
    '10': '服飾',
    '12': '租金',
    '8': 'fun',
    '15': 'Medical',
    '20': 'other',
    '9': 'social',
    '29': '罰單',
}

for item in backup['tables'][0]['items'][::-1]:
    # if item['date'] == '2019-11-24':
    #     print(item)
    # if item['descr'] == '鎖匠':
    #     print(item)
    pass



result = {
    item['category_id']: [x['descr'] for x in backup['tables'][0]['items'] if x['category_id'] == item['category_id'] and x['descr']] for item in backup['tables'][0]['items']
}
for category_id, descr_list in result.items():
    if category_id not in ['11']:
        continue
    print(f"====={category_id}=====")
    for descr in descr_list[:]:
        print(descr)

gg = {
    'table_setting': {
        'category': [
            {'name': '飲食', 'sub_category': ['預設', '晚餐', '早餐', '午餐', '零食', '飲料', '酒']},
            {'name': '交通', 'sub_category': ['預設', '停車費', '捷運', '悠遊卡', '火車', '公車', '高鐵', '汽油', 'I-Rent', 'Wemo', 'GoShare', '過路費']},
            {'name': '娛樂', 'sub_category': ['預設', '電影', '遊戲', '小說']},
            {'name': '運動', 'sub_category': ['預設', '足球', '羽球', '溜冰', '衝浪', '攀岩', '潛水', '健身房', '游泳', '桌球']},
            {'name': '服飾', 'sub_category': ['預設', '化妝品']},
            {'name': '購物', 'sub_category': ['預設', '3C', '電腦', '必需品', '生活品質']},
            {'name': '投資', 'sub_category': ['預設', '保險', '專業', '股票', '基金']},
            {'name': '帳單', 'sub_category': ['預設', '水費', '電費', '房租', '電話費']},
            {'name': '社交', 'sub_category': ['預設']},
            {'name': '日常', 'sub_category': ['預設', '日常用品', '剪頭髮', '隱形眼鏡']},
            {'name': '禮物', 'sub_category': ['預設', '禮金', '票券', '幫出錢']},
            {'name': '罰單', 'sub_category': ['預設', '汽車罰單', '機車罰單']},
            {'name': '旅遊', 'sub_category': ['預設', '住宿', '食物', '玩樂', '交通']},
            {'name': '醫療', 'sub_category': ['預設', '復健', '生病', '牙齒', '健康檢查']},
            {'name': '住宿', 'sub_category': ['預設', '家具', '租金', '清潔用品', '停車位']},
            {'name': '花錢消災', 'sub_category': ['預設']},
        ],
        'budget': 25000,
    },
    'items': [
        {
            'datetime': '2016-04-05 12:07:15',
            'amount': 120,
            'description': '',
            'category': [0, 3]
        },
    ]
}