from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.misc.states import Interview
from tgbot.keyboards import inline
from tgbot.services import datas
from tgbot.keyboards.callback_datas import service_callback
from tgbot.keyboards.callback_datas import stat_callback
from tgbot.keyboards.callback_datas import choice_callback
from tgbot.keyboards.callback_datas import support_callback


STAT_ANALYS_SERVICES = datas.stat_datas
STAT_FORECAST_SERVICES = datas.stat_datas_forecast


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

    keyboard = await inline.kb_stat_processing_choice(stat_datas)

    await call.message.edit_text(text='Выберете вид анализа', reply_markup=keyboard)
    await Interview.waiting_for_stat_processing_choice.set()
    await call.answer()


async def stat_price_answer(call: types.CallbackQuery, callback_data: dict,
                            state: FSMContext, stat_datas=STAT_ANALYS_SERVICES):
    choice = callback_data.get(("service"))
    keyboard = await inline.kb_discount()
    option = stat_datas[choice][0]
    bill = stat_datas[choice][1]

    await state.update_data(chosen_stat_processing=option)
    print(str(await state.get_data()))

    if choice in ["data_descr", "comparing"]:
        await call.message.edit_text(
                            text=f"Вы выбрали: {option}.\n"
                                 f"Ориентировочная стоимость услуги <u><b>{bill}</b></u> руб./показатель.\n"
                                 f"Чтобы получить точный расчет стоимости для вас, пришлите "
                                 f"Ваши данные на почту aeo@statzilla.ru. \nОБЯЗАТЕЛЬНО в письме "
                                 f"напишите ответ на вопросы ниже:\n- Какие группы Вы рассматриваете, сколько их?\n"
                                 f"- В какой колонке в данных содержится информация о принадлежности к той или иной группе?\n"
                                 f"- Какие показатели должны быть включены в анализ?\n- В каких колонках они содержатся?",
                            parse_mode='HTML',
                            reply_markup=keyboard)
    elif choice == "survival_anls":
        await call.message.edit_text(
                            text=f"Вы выбрали: {option}.\n"
                                 f"Cтоимость услуги <u><b>{bill}</b></u> руб. за анализ 1 исхода в 1 группе\n"
                                 f"Чтобы получить точный расчет стоимости для вас, пришлите "
                                 f"Ваши данные на почту aeo@statzilla.ru. \nОБЯЗАТЕЛЬНО в письме "
                                 f"напишите ответ на вопросы ниже:\n- Что считается исходом в Вашем исследовании (положительным и отрицательным)?\n"
                                 f"- В какой колонке содержится информация об исходе?\n"
                                 f"- Какие показатели должны быть включены в анализ? В каких колонках они содержатся?\n"
                                 f"- Нужно ли делать сравнение выживаемости в группах? Каких?",
                            parse_mode='HTML',
                            reply_markup=keyboard)
    elif choice == "correlation":
        await call.message.edit_text(
                            text=f"Вы выбрали: {option}.\n"
                                 f"Cтоимость услуги <u><b>{bill}</b></u> руб./1 пара показателей.\n"
                                 f"Чтобы получить точный расчет стоимости для вас, пришлите "
                                 f"Ваши данные на почту aeo@statzilla.ru. \nОБЯЗАТЕЛЬНО в письме "
                                 f"напишите ответ на вопросы ниже:\n"
                                 f"- Какие показатели должны быть включены в анализ? В каких колонках они содержатся?\n"
                                 f"- Нужно ли делать сравнение коэффициентов корреляций в группах? Каких?",
                            parse_mode='HTML',
                            reply_markup=keyboard)
    elif choice == "risk_anls":
        await call.message.edit_text(
                            text=f"Вы выбрали: {option}.\n"
                                 f"Cтоимость услуги <u><b>{bill}</b></u> руб./отношения шансов и отношения рисков для 1 показателя.\n"
                                 f"Чтобы получить точный расчет стоимости для вас, пришлите "
                                 f"Ваши данные на почту aeo@statzilla.ru. \nОБЯЗАТЕЛЬНО в письме "
                                 f"напишите ответ на вопросы ниже:\n"
                                 f"- Риски/шансы чего Вы хотите оценить? В какой колонке содержится этот показатель?\n"
                                 f"- Какие факторы риска должны быть включены в анализ? В каких колонках они содержатся?",
                            parse_mode='HTML',
                            reply_markup=keyboard)
    elif choice == "cluster_anls":
        await call.message.edit_text(
                            text=f"Вы выбрали: {option}.\n"
                                 f"Cтоимость услуги <u><b>{bill}</b></u> руб. за 1 кластеризацию\n"
                                 f"Чтобы получить точный расчет стоимости для вас, пришлите "
                                 f"Ваши данные на почту aeo@statzilla.ru. \nОБЯЗАТЕЛЬНО в письме "
                                 f"напишите ответ на вопросы ниже:\n"
                                 f"- Какая у вас задача исследования? Что хотите показать с помощью кластеризации?\n"
                                 f"- Какие показатели должны быть включены в анализ? В каких колонках они содержатся?",
                            parse_mode='HTML',
                            reply_markup=keyboard)
    await Interview.price_answer.set()
    await call.answer()


async def stat_types_of_forecast(call: types.CallbackQuery,
                                 state: FSMContext,
                                 stat_datas=STAT_FORECAST_SERVICES):
    await state.update_data(chosen_stat_processing="Многофакторные модели прогноза")
    keyboard = await inline.kb_forecast_mdl(stat_datas)
    await call.message.edit_text(
                                text="Выбереите необходимую модель:",
                                reply_markup=keyboard)
    await Interview.waiting_for_stat_forecast_choice.set()
    await call.answer()


async def stat_forecast_price_answer(
    call: types.CallbackQuery, callback_data: dict,
    state: FSMContext, stat_datas=STAT_FORECAST_SERVICES
):
    choice = callback_data.get(("service"))
    keyboard = await inline.kb_discount()
    option = stat_datas[choice][0]
    bill = stat_datas[choice][1]

    await state.update_data(chosen_forecast_option=option)
    print(str(await state.get_data()))
    if choice == "dont_know":
        await call.message.edit_text(
            text=(
                "Пришлите Ваши данные на почту aeo@statzilla.ru. \n"
                "ОБЯЗАТЕЛЬНО в письме напишите ответ на вопросы ниже:\n"
                "- Какая у вас задача исследования, что хотите доказать?\n"
                "- Какие группы Вы рассматриваете, сколько их?\n"
                "- В какой колонке в данных содержится информация о "
                "принадлежности к той или иной группе?\n"
                "- Какие показатели должны быть включены в анализ? В каких "
                "колонках они содержатся?"
                "В ответ мы пришлем полный расчет стоимости для Вас."
            ),
            parse_mode='HTML',
            reply_markup=keyboard
        )
    else:
        await call.message.edit_text(
            text=(
                f"Вы выбрали: {option}.\n"
                f"Ориентировочная стоимость услуги <u><b>{bill}</b></u> руб.\n"
                f"пришлите Ваши данные на почту aeo@statzilla.ru. \n"
                f"ОБЯЗАТЕЛЬНО в письме напишите ответ на вопросы ниже:\n- Какая у вас задача исследования, что хотите доказать?\n"
                f"- Какой показатель вы хотите предсказать, в какой колонке он содержится?\n"
                f"- Какие показатели должны быть включены в анализ?\n- В каких колонках они содержатся?"
            ),
            parse_mode='HTML',
            reply_markup=keyboard
        )
    await Interview.price_answer.set()
    await call.answer()


async def stat_hypothesis(call: types.CallbackQuery):
    keyboard = await inline.kb_yes_no()
    await call.message.edit_text("У вас есть сформулированная гипотеза?", reply_markup=keyboard)
    await Interview.waiting_for_stat_hypothesis_choice.set()
    await call.answer()


async def stat_hypothesis_answer(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    choice = callback_data.get(("answer"))
    await state.update_data(have_hypothesis=choice)
    print(str(await state.get_data()))
    keyboard = await inline.kb_return_start()
    if choice == "Yes":
        await call.message.edit_text(
            text=(
                "Вам необходим дизайн исследования - это документ, который описывает, "
                "какие методы статистического анализа и в каком порядке использовать "
                "конкретно на Ваших данных, чтобы доказать Вашу гипотезу. Он также дает "
                "ответ на вопрос, какой размер выборки Вам нужен, то есть достаточно ли "
                "у Вас данных; т.е. если у Вас уже есть данные и Вы понимаете что хотите "
                "увидеть на выходе (что доказать). \nСтоимость <u><b>8000</b></u> руб."
                "\nПришлите Вашу тему и наработки (если они есть) на почту aeo@statzilla.ru/"
            ),
            reply_markup=keyboard
        )
    else:
        await call.message.edit_text(
            text=(
                "Вам необходим разведочный анализ - это глубинный поисковой анализ всех "
                "ваших данных. Он позволит выявить что есть интересного в ваших данных, "
                "какие существуют связи и зависимости. На основе этой информации Вы сможете "
                "сформулировать научную гипотезу и тему исследования; т.е. если у Вас есть "
                "данные, но нет понимания, что Вы хотите на выходе. Мы предлагаем Вам варианты."
                "\nСтоимость <u><b>10000</b></u> руб."
                "\nПришлите Вашу тему и наработки (если они есть) на почту aeo@statzilla.ru/"
            ),
            reply_markup=keyboard
        )
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
        stat_types_of_forecast,
        stat_callback.filter(service="forecast_mdl"),
        state=Interview.waiting_for_stat_processing_choice
        )
    dp.register_callback_query_handler(
        stat_price_answer,
        stat_callback.filter(),
        state=Interview.waiting_for_stat_processing_choice
        )
    dp.register_callback_query_handler(
        stat_forecast_price_answer,
        stat_callback.filter(),
        state=Interview.waiting_for_stat_forecast_choice
        )
    dp.register_callback_query_handler(
        stat_hypothesis,
        choice_callback.filter(answer="No"),
        state=Interview.waiting_for_stat_types_yes_answer
        )
    dp.register_callback_query_handler(
        stat_hypothesis,
        support_callback.filter(messages="dont_know"),
        state=Interview.waiting_for_stat_processing_choice
        )
    dp.register_callback_query_handler(
        stat_hypothesis_answer,
        choice_callback.filter(),
        state=Interview.waiting_for_stat_hypothesis_choice
        )
