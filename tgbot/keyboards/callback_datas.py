from aiogram.utils.callback_data import CallbackData

service_callback = CallbackData("service", "main_services")
stat_callback = CallbackData("stat", "service")
back_callback = CallbackData("back", "deep")
help_callback = CallbackData("help", "user_id")
choice_callback = CallbackData("choice", "answer")

support_callback = CallbackData("ask_support", "messages")
cancel_support_callback = CallbackData("cancel_support", "user_id")
