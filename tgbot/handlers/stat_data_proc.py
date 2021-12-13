from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.misc.states import Interview
from tgbot.keyboards import inline
from tgbot.services import datas
from tgbot.keyboards.callback_datas import service_callback
from tgbot.keyboards.callback_datas import stat_callback
from tgbot.keyboards.callback_datas import choice_callback


async def stat_processing_choice(call: types.CallbackQuery,
                                 callback_data: dict,
                                 state: FSMContext):
    """Функция вызываемая только из состояния waiting_for_service_selection"""
    keyboard = await inline.kb_yes_no()

    await state.update_data(chosen_main_service="Статистическая обработка")
    print(callback_data)
    print(await state.get_data())

    await call.message.edit_text(text="Есть ли у вас данные?",
                                 reply_markup=keyboard)
    await Interview.waiting_for_stat_yes_no_answer.set()

    '''if service_choise == "stat_proc":
        await call.message.edit_text(text="Теперь выберите вид анализа:",
                                     reply_markup=keyboard)
        await Interview.waiting_for_stat_processing_choice.set()
    else:
        await call.message.answer(text="пока не написал код")
        await state.finish()'''

    await call.answer()


async def stat_have_datas(call: types.CallbackQuery,
                          state: FSMContext):
    keyboard = await inline.kb_yes_no()
    await state.update_data(have_data="Да")
    print(await state.get_data())
    await call.message.edit_text(text="Знаете ли Вы какие виды анализа нужны?",
                                 reply_markup=keyboard)
    await Interview.waiting_for_stat_types_yes_no_answer.set()
    await call.answer()


async def stat_havent_datas(call: types.CallbackQuery,
                            state: FSMContext):
    keyboard = await inline.kb_yes_no()
    await state.update_data(have_data="Нет")
    print(await state.get_data())
    await call.message.edit_text(text="Кракозябра")
    await call.message.answer("https://docs.google.com/spreadsheets/d/1xg4KaPw-amRCGW5RYAqKmU26Z5R6THVM/edit?usp=sharing&ouid=114362960612507406007&rtpof=true&sd=true")

    await Interview.waiting_for_stat_types_yes_no_answer.set()
    await call.answer()


async def stat_price_answer(call: types.CallbackQuery, callback_data: dict,
                            state: FSMContext):
    choice = callback_data.get(("service"))
    user_id = call.from_user.id
    keyboard = await inline.kb_discount(user_id)
    option = datas.stat_datas[choice][0]
    bill = datas.stat_datas[choice][1]

    await state.update_data(chosen_stat_processing=choice)
    await call.message.edit_text(
                            text=f"Вы выбрали: {option} стоимость составит:\n"
                                 f"<u><b>{bill}</b></u> р.",
                            parse_mode='HTML',
                            reply_markup=keyboard)
    await Interview.price_answer.set()
    await call.answer()


def register_analysis(dp: Dispatcher):
    dp.register_callback_query_handler(
        stat_processing_choice,
        service_callback.filter(main_services="stat_proc"),
        state=Interview.waiting_for_service_selection
        )
    dp.register_callback_query_handler(
        stat_have_datas,
        choice_callback.filter(answer="Yes"),
        state=Interview.waiting_for_stat_yes_no_answer
        )
    dp.register_callback_query_handler(
        stat_havent_datas,
        choice_callback.filter(answer="No"),
        state=Interview.waiting_for_stat_yes_no_answer
        )
    dp.register_callback_query_handler(
        stat_price_answer,
        stat_callback.filter(),
        state=Interview.waiting_for_stat_processing_choice
        )
