from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from tgbot.keyboards import inline
from tgbot.misc.states import Interview


async def interview_start(message: types.Message, state: FSMContext):
    """Обработчик первого шага, реагирующий на команду start"""
    await state.finish()

    user_name = message.from_user.first_name

    await message.answer(text=f"Приветствую, {user_name}!",
                         reply_markup=types.ReplyKeyboardRemove())
    keyboard = await inline.kb_service_selection()
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
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel,
                                Text(equals="отмена", ignore_case=True),
                                state="*")
