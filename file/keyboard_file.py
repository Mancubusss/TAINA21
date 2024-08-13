from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types

def admin_cancel():
    keyboard = InlineKeyboardMarkup(row_width=2)
    hide = InlineKeyboardButton(text="◀️ Отмена", callback_data="cancel")
    keyboard.add(hide)
    return keyboard




def start_menu(dict_c):
    btns = []
    for i in dict_c:
        btns.append(InlineKeyboardButton(text=i, url=dict_c[i]))

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*btns)
    return keyboard

def menu_adm():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn = InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
    btn1 = InlineKeyboardButton(text="📣 Рассылка", callback_data="rasilka")
    keyboard.add(btn, btn1)
    return keyboard

def admin_menu(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn = InlineKeyboardButton(text="✅ Одобрить", callback_data=f"yes;{user_id}")
    btn1 = InlineKeyboardButton(text="❌ Отклонить", callback_data=f"no;{user_id}")
    keyboard.add(btn, btn1)
    return keyboard


def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn = InlineKeyboardButton(text="✅ Отправить", callback_data="succ")
    btn1 = InlineKeyboardButton(text="🔁 Изменить", callback_data="restart")
    keyboard.add(btn, btn1)
    return keyboard

