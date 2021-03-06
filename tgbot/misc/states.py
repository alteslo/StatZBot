from aiogram.dispatcher.filters.state import State, StatesGroup


class Interview(StatesGroup):
    waiting_for_service_selection = State()
    waiting_for_stat_yes_no_answer = State()
    waiting_for_stat_types_yes_answer = State()
    waiting_for_stat_types_no_answer = State()
    waiting_for_stat_processing_choice = State()
    waiting_for_stat_forecast_choice = State()
    waiting_for_stat_hypothesis_choice = State()
    price_answer = State()

    waiting_for_contact_number = State()
    wait_for_support_message = State()
