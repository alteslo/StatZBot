from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

from tgbot.misc.states import Interview
from tgbot.keyboards import inline

from tgbot.keyboards.callback_datas import service_callback


async def presentation_choice(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_main_service="Презентация")
    print(str(await state.get_data()))
    keyboard = await inline.kb_return_start()
    await call.message.edit_text(
        text=(
            "Вы выбрали презентацию. Стоимость от <b><u>500</u></b> руб."
            "/слайд (стоимость формируется после уточнения объема и темы). \n"
            "Пришлите Вашу тему и наработки (если они есть) на почту "
            "aeo@statzilla.ru"
        ),
        reply_markup=keyboard
    )
    await call.answer()


def register_presentation(dp: Dispatcher):
    dp.register_callback_query_handler(
        presentation_choice,
        service_callback.filter(main_services="other"),
        state=Interview.waiting_for_service_selection
    )
