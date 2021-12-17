from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import message

from tgbot.misc.states import Interview
from tgbot.keyboards import inline
from tgbot.services import datas
from tgbot.keyboards.callback_datas import service_callback
from tgbot.keyboards.callback_datas import stat_callback
from tgbot.keyboards.callback_datas import choice_callback


STAT_ANALYS_SERVICES = datas.stat_datas


async def stat_processing_choice(call: types.CallbackQuery,
                                 callback_data: dict,
                                 state: FSMContext):
    """1 вопрос опроса функция вызываемая только из состояния waiting_for_service_selection"""
    keyboard = await inline.kb_yes_no()

    await state.update_data(chosen_main_service="Статистическая обработка")
    await call.message.edit_text(text="Есть ли у вас данные?",
                                 reply_markup=keyboard)
    await Interview.waiting_for_stat_yes_no_answer.set()
    await call.answer()


async def stat_have_datas(call: types.CallbackQuery,
                          state: FSMContext):
    """Есть данные состояние waiting_for_stat_yes_no_answer"""
    keyboard = await inline.kb_yes_no()
    await state.update_data(have_data="Да")

    print(await state.get_data())

    await call.message.edit_text(text="Знаете ли Вы какие виды анализа нужны?",
                                 reply_markup=keyboard)
    await Interview.waiting_for_stat_types_yes_answer.set()
    await call.answer()


async def stat_havent_datas(call: types.CallbackQuery,
                            state: FSMContext):
    """Нет данных состояние waiting_for_stat_yes_no_answer"""
    text = ("Для статистической обработки необходимо собрать данные. \n"
            "Для того чтобы Вам было удобнее мы подготовили для Вас шаблон "
            "базы данных и памятку по данным. \nТак Вы сможете формировать "
            "данные сразу в необходимом формате для статистической обработки."
            "\nСкачать их можно ниже")
    keyboard = await inline.kb_return_start()

    await state.update_data(have_data="Нет")

    print(await state.get_data())

    await call.message.edit_text(text=text)
    await call.message.answer("https://docs.google.com/spreadsheets/d/1xg4KaPw-amRCGW5RYAqKmU26Z5R6THVM/edit?usp=sharing&ouid=114362960612507406007&rtpof=true&sd=true")
    await call.message.answer_photo(
                            types.InputFile('tgbot/misc/Памятка_данных.png'),
                            caption='Памятка',
                            reply_markup=keyboard)

    await Interview.waiting_for_stat_types_no_answer.set()
    await call.answer()


async def stat_types_of_analyses(
                                call: types.CallbackQuery,
                                state: FSMContext,
                                stat_datas=STAT_ANALYS_SERVICES):
    '''Выбор видов анализа состояние waiting_for_stat_types_yes_answer'''
    await state.update_data(know_types_anls="Да")

    print(await state.get_data())

    user_id = call.from_user.id
    keyboard = await inline.kb_stat_processing_choice(user_id, stat_datas)

    await call.message.edit_text(text='Выберете вид анализа', reply_markup=keyboard)
    await Interview.waiting_for_stat_processing_choice.set()
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
        stat_types_of_analyses,
        choice_callback.filter(answer="Yes"),
        state=Interview.waiting_for_stat_types_yes_answer
        )
    dp.register_callback_query_handler(
        stat_price_answer,
        stat_callback.filter(),
        state=Interview.waiting_for_stat_processing_choice
        )
