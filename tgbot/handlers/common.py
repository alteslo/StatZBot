from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from tgbot.keyboards import inline
from tgbot.misc.states import Interview
from tgbot.config import Config


async def interview_start(message: types.Message, state: FSMContext):
    """Обработчик первого шага, реагирующий на команду start"""
    await state.finish()

    user_name = message.from_user.first_name

    await message.answer(text=f"Приветствую, {user_name}!",
                         reply_markup=types.ReplyKeyboardRemove())
    config: Config = message.bot.get("config")
    id_manager = config.tg_bot.support_ids
    keyboard = await inline.kb_service_selection(id_manager[0])
    await message.answer(text="Какую услугу вы хотите получить?",
                         reply_markup=keyboard)

    await Interview.waiting_for_service_selection.set()


# Уточнить нужен ли подобный функционал
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Действие отменено",
                         reply_markup=types.ReplyKeyboardRemove())


def register_common(dp: Dispatcher):
    dp.register_message_handler(interview_start, commands="start", state="*")
