from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

from tgbot.misc.states import Interview
from tgbot.keyboards import inline
from tgbot.services.google_sheets import create_spreadsheet, add_worksheet, share_spreadsheet, fill_in_data
from tgbot.keyboards.callback_datas import service_callback


async def lit_rev_choice(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_main_service="Литобзор")
    print(str(await state.get_data()))

    keyboard = await inline.kb_return_start()
    await call.message.edit_text(
        text=(
            "Вы выбрали литобзор. Мы работаем в 2 этапа:\n"
            "1) Предварительный ресерч (формируем список литературы, "
            "согласуем его с Вами + считаем стоимость полного объема работы)"
            "стоимость <u><b>2000</b></u> руб.\n"
            "2) Написание самого литобзора\n"
            "Пришлите Вашу тему и наработки (если они есть) на почту "
            "aeo@statzilla.ru"
        ),
        reply_markup=keyboard
    )
    await call.answer()
    state_data = await state.get_data()
    data = tuple((state_data.values()))
    print(data)
    # data = (("1", "2", "3", "4", "5"), ())
    google_client_manager = call.bot.get('google_client_manager')
    google_client = await google_client_manager.authorize()
    key = '1lv-kpvCo66N8ynKl1wdLdh8q6NXwtxhQvzgJwh6Cf_8'
    spreadsheet = await google_client.open_by_key(key)
    worksheet = await spreadsheet.worksheet('Sheet6')
    await fill_in_data(worksheet, data, headers=['ID', 'Name', 'Phone', 'Address', 'Orders Amount'])


def register_lit_rev(dp: Dispatcher):
    dp.register_callback_query_handler(
        lit_rev_choice,
        service_callback.filter(main_services="lit_rev"),
        state=Interview.waiting_for_service_selection
    )
