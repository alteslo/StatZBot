from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext

from tgbot.misc.states import Interview
from tgbot.keyboards import inline
from tgbot.services import datas
from tgbot.keyboards.callback_datas import back_callback
from tgbot.config import Config


STAT_ANALYS_SERVICES = datas.stat_datas


async def return_to_stat_processing_choice(call: types.CallbackQuery,
                                           callback_data: dict,
                                           state: FSMContext,
                                           stat_datas=STAT_ANALYS_SERVICES):
    # Подумать о сбросе состояния
    await state.update_data(chosen_stat_processing="")

    choice = callback_data.get(("deep"))

    if choice == "stat_choice":
        keyboard = await inline.kb_stat_processing_choice(stat_datas)
        await call.message.edit_text(text="Выберите вид анализа:",
                                     reply_markup=keyboard)
        await state.reset_state()
        await Interview.waiting_for_stat_processing_choice.set()
    elif choice == "start":
        config: Config = call.bot.get("config")
        id_manager = config.tg_bot.support_ids
        keyboard = await inline.kb_service_selection(*id_manager)
        if str(await state.get_state()) in ['Interview:waiting_for_stat_types_no_answer']:
            photo_src = types.InputFile('tgbot/misc/Памятка_данных.png')
            await call.message.answer_photo(photo_src)
            await call.message.answer(text="Какую услугу вы хотите получить?",
                                      reply_markup=keyboard)
        else:
            await call.message.edit_text(
                text="Какую услугу вы хотите получить?",
                reply_markup=keyboard)
        # Был финиш стэйт
        await state.reset_state()
        await Interview.waiting_for_service_selection.set()
    await call.answer()


def register_return(dp: Dispatcher):
    dp.register_callback_query_handler(return_to_stat_processing_choice,
                                       back_callback.filter(),
                                       state="*")
