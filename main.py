# ----------------------------------------------------------------------------------------
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputFile, InputMediaPhoto
from aiogram.utils.exceptions import Throttled
import logging
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
import re
import time
# ----------------------------------------------------------------------------------------
import file.db_file as db
import file.keyboard_file as kb
from file.state_file import *
import config as cfg
# ----------------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=cfg.bot_token, parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(bot, storage=MemoryStorage())
# ----------------------------------------------------------------------------------------



async def start_main(x):
    global bot_username
    await db.check_start("db.db")
    bot_username = (await bot.get_me()).username

    




@dp.message_handler(commands="admin", state="*", content_types=["text"], chat_type=["private"], user_id=cfg.admin_id)
async def admin_welcom(message: types.Message, state: FSMContext):
    await message.answer("Админ меню", reply_markup=kb.menu_adm())


@dp.callback_query_handler(user_id=cfg.admin_id, chat_type=["private"], text=["stats"], state="*")
async def sss1(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    days, week, month, all_ = await db.get_info()
    await call.message.answer(f"""<b>
Статистика проекта @{bot_username}

1️⃣ Пользователей за сегодня: <code>{days}</code>
2️⃣ Пользователей за неделю: <code>{week}</code>
3️⃣ Пользователей за месяц: <code>{month}</code>
4️⃣ Всего пользователей: <code>{all_}</code>
</b>""", reply_markup=kb.admin_cancel())


@dp.callback_query_handler(user_id=cfg.admin_id, text="rasilka", state="*")
async def sss2(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("Введите сообщение для рассылки:", reply_markup=kb.admin_cancel())
    await state.update_data(msg=msg)
    await Rasilka.msg.set()



@dp.message_handler(user_id=cfg.admin_id, state=Rasilka.msg, content_types=["any"])
async def sss3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg = data["msg"]
    await msg.delete()
    await state.finish()
    await message.answer("Начинаю рассылку!", reply_markup=kb.menu_adm())

    users = await db.get_users()
    valid = 0
    nevalid = 0

    for user in users:
        try:
            await message.copy_to(chat_id=user[0])
            valid += 1
        except:
            nevalid += 1

    await message.answer(f"""
ℹ️ Рассылка закончена

✅ Успешно отправлено: <code>{valid}</code>
❌ Ошибок при отправке: <code>{nevalid}</code>
👥 Всего юзеров: <code>{len(users)}</code>""")



@dp.callback_query_handler(user_id=cfg.admin_id, text="cancel", state="*")
async def sss(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Добро пожаловать в админ меню!", reply_markup=kb.menu_adm())

@dp.message_handler(commands="start", state="*", content_types=["text"], chat_type=["private"])
async def start(message: types.Message, state: FSMContext):
    await db.add_db(message.from_user.id, message.from_user.username, time.time())
    
    user = await db.get_user(message.from_user.id)
    if user:
        if user[2] == 1:
            await message.answer(f"<b>Приветствую тебя, {message.from_user.first_name}</b>", reply_markup=kb.start_menu(cfg.links))
            return
        elif user[2] == 2:
            await message.answer("<b>⏳ Вы уже подавали заявку!</b>")
            return
        elif user[2] == 3:
            await message.answer("<b>📛 Вам отклонили заявку!</b>")
            return


    data = {
        "num": 0,
        "message": "<b>👤 Ваша заявка:</b>\n\n",
        "photos": []
    }
    await message.answer("<b>"+list(cfg.question)[int(data["num"])]+"</b>")

    await state.update_data(question_dict=data)
    await States.question.set()


@dp.message_handler(state=States.question, content_types=["text"])
async def ss(message: types.Message, state: FSMContext):



    data = await state.get_data()
    data = data["question_dict"]

    
    old_quest = list(cfg.question)[int(data["num"])]

    
    
    data["num"] += 1


    data["message"] += f"<b>{data['num']}) {old_quest}: <code>{message.text}</code></b>" + "\n"
    
    await state.update_data(question_dict=data)
    
    if int(data["num"]) != len(cfg.question):

        quest = cfg.question[int(data["num"])]
        await message.answer("<b>"+quest+"</b>")
        return
    
    await state.finish()
    await message.answer(text=data["message"], reply_markup=kb.main_menu())
    



@dp.callback_query_handler(text=["restart"], state="*")
async def ss1(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = await db.get_user(call.from_user.id)
    if user:
        if user[2] == 1:
            await call.answer("✅ Вам уже одобрили заявку")
            return
        elif user[2] == 2:
            await call.answer("⏳ Вы уже подавали заявку!")
            return
        elif user[2] == 3:
            await call.answer("📛 Вам отклонили заявку!")
            return
    await call.message.delete()
    data = {
        "num": 0,
        "message": "<b>👤 Ваша заявка:</b>\n\n",
        "photos": []
    }
    await call.message.answer("<b>"+list(cfg.question)[int(data["num"])]+"</b>")

    await state.update_data(question_dict=data)
    await States.question.set()

@dp.callback_query_handler(text=["succ"], state="*")
async def ss2(call: types.CallbackQuery, state: FSMContext):
    user = await db.get_user(call.from_user.id)
    if user:
        if user[2] == 1:
            await call.answer("✅ Вам уже одобрили заявку")
            return
        elif user[2] == 2:
            await call.answer("⏳ Вы уже подавали заявку!")
            return
        elif user[2] == 3:
            await call.answer("📛 Вам отклонили заявку!")
            return
    msg = call.message.text.replace("👤 Ваша заявка:", f"<b>🎉 Новая заявка: @{call.from_user.username} (<code>{call.from_user.id}</code>)</b>")
    regx = re.findall(": (.*)", msg)[1:]
    for i in regx:
        msg = msg.replace(i, f"<code>{i}</code>")
    msg = "<b>" + msg +"</b>"
    
    
    await bot.send_message(chat_id=cfg.admin_id, text=msg, reply_markup=kb.admin_menu(call.from_user.id))
    await db.set_limit(call.from_user.id, 2)
    await call.message.delete()


@dp.callback_query_handler(text_contains=["yes;"], state="*")
async def ss3(call: types.CallbackQuery, state: FSMContext):
    s, user_id = call.data.split(";")
    await call.answer("Оповестил пользователя!")
    await call.message.edit_reply_markup(None)

    try:
        await bot.send_message(user_id, "<b>🔥 Вам одобрили заявку!</b>", reply_markup=kb.start_menu(cfg.links))
    except:
        pass
    await db.set_limit(user_id, 1)

@dp.callback_query_handler(text_contains=["no;"], state="*")
async def ss4(call: types.CallbackQuery, state: FSMContext):
    s, user_id = call.data.split(";")
    await call.answer("Оповестил пользователя!")
    await call.message.edit_reply_markup(None)

    try:
        await bot.send_message(user_id, "<b>🔥 Вам отклонили заявку!</b>")
    except:
        pass

    await db.set_limit(user_id, 3)



if __name__ == '__main__':
    try:

        executor.start_polling(dp, skip_updates=True, on_startup=start_main)

    except Exception as err:
        print(err)


