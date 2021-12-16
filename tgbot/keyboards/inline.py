from aiogram import types

from tgbot.services.datas import stat_datas
from tgbot.keyboards.callback_datas import service_callback
from tgbot.keyboards.callback_datas import stat_callback
from tgbot.keyboards.callback_datas import back_callback
from tgbot.keyboards.callback_datas import help_callback
from tgbot.keyboards.callback_datas import choice_callback


async def kb_service_selection(width=1):
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
                                        main_services="other"))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=width)
    keyboard.add(*buttons)
    return keyboard


async def kb_stat_processing_choice(user_id, width=1):
    """Клавиатура для выбора услуг статистического анализа"""
    buttons = []
    for key in stat_datas:
        buttons.append(
            types.InlineKeyboardButton(text=stat_datas.get(key)[0],
                                       callback_data=stat_callback.new(
                                                    service=key)))

    buttons.append(
        types.InlineKeyboardButton(text="Не нашли подходящий инструмент?",
                                   callback_data=help_callback.new(
                                       user_id=user_id))
    )
    keyboard = types.InlineKeyboardMarkup(row_width=width)
    keyboard.add(*buttons)
    return keyboard


async def kb_discount(user_id, width=1):
    """Клавиатура для выбора услуг статистического анализа"""
    buttons = [
            types.InlineKeyboardButton(text="Хотите скидку?",
                                       callback_data=help_callback.new(
                                            user_id=user_id)),
            types.InlineKeyboardButton(text="Вернуться к выбору услуг",
                                       callback_data=back_callback.new(
                                            deep="stat_choice")),
            types.InlineKeyboardButton(text="Вернуться к началу",
                                       callback_data=back_callback.new(
                                            deep="start"))

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
