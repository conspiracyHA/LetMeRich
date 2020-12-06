from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from CategoryManager import CategoryManager
from ItemManager import ItemManager
from Utility.Path import path_join
from datetime import datetime
from functools import wraps
import logging
import re
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

with open(path_join('bot_token.txt')) as f:
    bot_token = f.readline()

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
item_manager = ItemManager()
cat_manager = CategoryManager()


def using_command(command):
    def assign_command(func):
        dispatcher.add_handler(CommandHandler(command, func))
    return assign_command


@using_command('start')
def start_handler(update, context):
    print(f'start called by {update.message.chat.first_name}')
    # print(f'username {update.message.chat.username}')
    # print(f'first_name {update.message.chat.first_name}')
    # print(f'last_name {update.message.chat.last_name}')
    first_name = update.message.chat.first_name
    text = f'哈囉，{first_name}\n' \
           '只要輸入 \"午餐 200\"\n' \
           '我就可以幫您紀錄唷\n' \
           '詳細的使用方法請點 /help\n' \
           '查看有什麼分類請點 /category'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


@using_command('category')
def category_handler(update, context):
    print(f'start called by {update.message.chat.first_name}')
    cat2subcats = cat_manager.get_all_category()
    text = '您目前的主分類有:\n'
    for idx, (cat, subcats) in enumerate(cat2subcats.items(), start=1):
        text += f"{idx:2}.  {cat}\n"
    text += '\n如想看子分類\n' \
            '請輸入 \"查看{主分類}\"'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


@using_command('gg')
def gg_handler(update, context):
    print(f'start called by {update.message.chat.first_name}')
    text = 'gg的參數是: ' + ', '.join(context.args)
    print(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


@using_command('help')
def help_handler(update, context):
    print(f'start called by {update.message.chat.first_name}')
    text = "記帳的方式有4種\n" \
           "1. 輸入 {子類別} {金額}\n" \
           "2. 輸入 {子類別} {金額} {備註}\n" \
           "3. 輸入 {類別} {子類別} {金額\n" \
           "4. 輸入 {類別} {子類別} {金額} {備註}\n" \
           "如果要查有哪些類別子類別 請點 /category"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


handlers = list()


def add_handler(func):
    handlers.append(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@add_handler
def handle_insert_item(input_text):
    descr = ''
    cat = None
    amount = ''
    subcat = ''
    idontknow = input_text.split(' ')
    if len(idontknow) == 2:
        subcat, amount = idontknow

    if len(idontknow) == 3:
        match = re.match(f'(\d+)元?', idontknow[2])
        if match:
            cat, subcat, amount = idontknow
        else:
            subcat, amount, descr = idontknow

    if len(idontknow) == 4:
        cat, subcat, amount, descr = idontknow

    amount = re.match(f'(\d+)元?', amount)
    if amount is None:
        return None
    amount = int(float(amount.group(1)))
    try:
        cat_name, cat_str = cat_manager.get_cat_idx_str(subcat, cat=cat)
    except ValueError as e:
        print(f'有人說: {input_text}，卻{str(e)}')
        return None

    date_str = datetime.now().strftime('%Y-%m-%d')
    item_manager.insert_item(date_str, cat_str, amount, descr)

    text = f'好的，\n{cat_name} {subcat} \n支出: {amount}，\n已幫您紀錄！'
    return text


@add_handler
def handle_search_subcat(input_text):
    idx = input_text.find('查看')
    if idx == -1:
        return None
    if idx + 2 >= len(input_text):
        return '我不知道要查看什麼欸'
    target = input_text[idx + 2:]
    cat2subcats = cat_manager.get_all_category()
    if target not in cat2subcats:
        return f'主分類中沒有\"{target}\"唷'

    text = f'在\"{target}\"有:\n'
    for idx, subcat in enumerate(cat2subcats[target], start=1):
        text += f"{idx:2}.  {subcat}\n"
    return text


def message_handler(update, context):
    # attrs = [
    #     'update_id', 'message', 'edited_message', 'channel_post',
    #     'edited_channel_post', 'inline_query', 'chosen_inline_result',
    #     'callback_query', 'shipping_query', 'pre_checkout_query', 'poll',
    #     'poll_answer', 'effective_chat', 'effective_message', 'effective_user'
    # ]
    # for attr in attrs:
    #     if attr != 'message':
    #         continue
    #     print(f'{attr}: {getattr(update, attr)}')
    input_text = update.message.text
    print(f'{update.message.chat.first_name}說:\n{update.message.text}')
    for handler in handlers:
        return_text = handler(input_text)
        if return_text is not None:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=return_text)
            return
    return_text = '不好意思我不知道你在公三小QQ'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=return_text)


dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
updater.start_polling()
