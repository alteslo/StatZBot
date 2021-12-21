from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

from tgbot.misc.states import Interview
from tgbot.keyboards import inline

from tgbot.keyboards.callback_datas import service_callback


async def lit_rev_choice(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
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


def register_lit_rev(dp: Dispatcher):
    dp.register_callback_query_handler(
        lit_rev_choice,
        service_callback.filter(main_services="lit_rev"),
        state=Interview.waiting_for_service_selection
    )
