from aiogram import types
# import datetime

from tgbot.keyboards.callback_datas import service_callback
from tgbot.keyboards.callback_datas import stat_callback
from tgbot.keyboards.callback_datas import back_callback
from tgbot.keyboards.callback_datas import choice_callback
from tgbot.keyboards.callback_datas import support_callback


async def kb_service_selection(manager):
    """Клавиатура для основного выбора услуг"""
    buttons = [
        types.InlineKeyboardButton(text="Статистическая обработка данных",
                                   callback_data=service_callback.new(
                                       main_services="stat_proc")),
        types.InlineKeyboardButton(text="Литобзор",
                                   callback_data=service_callback.new(
                                        main_services="lit_rev")),
        types.InlineKeyboardButton(text="Презентация",
                                   callback_data=service_callback.new(
                                        main_services="other")),
        types.InlineKeyboardButton(text="Напишите нашему менеджеру",
                                   url=f"https://t.me/{manager}")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    '''keyboard.add(
            types.InlineKeyboardButton(
                text="Напишите нашему менеджеру",
                url=f"tg://user?id={id_manager}"
                )
            )'''
    '''num_day = datetime.datetime.today().weekday()
    if num_day not in [5, 6]:
        keyboard.add(
            types.InlineKeyboardButton(
                text="Напишите нашему менеджеру",
                url=f"tg://user?id={id_manager}"
                )
            )'''
    return keyboard


async def kb_stat_processing_choice(stat_datas: dict):
    """Клавиатура для выбора услуг статистического анализа"""
    buttons = []
    for key in stat_datas:
        buttons.append(
            types.InlineKeyboardButton(
                text=stat_datas.get(key)[0],
                callback_data=stat_callback.new(service=key)
            )
        )
    buttons.append(
        types.InlineKeyboardButton(
            text="Я не знаю какой анализ мне нужен",
            callback_data=support_callback.new(messages="dont_know")
        )
    ),
    buttons.append(
        types.InlineKeyboardButton(
            text="Вернуться к началу",
            callback_data=back_callback.new(deep="start")
        )
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


async def kb_discount(width=1):
    """Клавиатура для выбора услуг статистического анализа"""
    buttons = [
            types.InlineKeyboardButton(
                text="Вернуться к выбору услуг",
                callback_data=back_callback.new(deep="stat_choice")
            ),
            types.InlineKeyboardButton(
                text="Вернуться к началу",
                callback_data=back_callback.new(deep="start")
            )
        ]
    keyboard = types.InlineKeyboardMarkup(row_width=width)
    keyboard.add(*buttons)
    return keyboard


async def kb_yes_no(width=1):
    """Клавиатура для выбора ответа (да или нет)"""
    buttons = [
            types.InlineKeyboardButton(text="Да",
                                       callback_data=choice_callback.new(
                                            answer="Yes")),
            types.InlineKeyboardButton(text="Нет",
                                       callback_data=choice_callback.new(
                                            answer="No"))
        ]
    keyboard = types.InlineKeyboardMarkup(row_width=width)
    keyboard.add(*buttons)
    return keyboard


async def kb_return_start():
    """Клавиатура для возврата к предыдущим пунктам меню"""
    buttons = [
            types.InlineKeyboardButton(text="Вернуться в начало",
                                       callback_data=back_callback.new(
                                            deep="start"))
        ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


async def kb_forecast_mdl(stat_datas: dict):
    buttons = []
    for key in stat_datas:
        buttons.append(
            types.InlineKeyboardButton(text=stat_datas.get(key)[0],
                                       callback_data=stat_callback.new(
                                                    service=key)))
    buttons.append(
        types.InlineKeyboardButton(text="Вернуться к выбору услуг",
                                   callback_data=back_callback.new(
                                            deep="stat_choice"))
    )
    buttons.append(
        types.InlineKeyboardButton(text="Вернуться к началу",
                                   callback_data=back_callback.new(
                                            deep="start"))
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
