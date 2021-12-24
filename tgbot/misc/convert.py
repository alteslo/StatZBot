import datetime
from aiogram import types


async def gsheet_add_data(call: types.CallbackQuery, state_data: dict):
    gsheet_dict = {
        'chosen_main_service': None, 'have_data': None,
        'know_types_anls': None, 'have_hypothesis': None,
        'chosen_stat_processing': None, 'chosen_forecast_option': None
    }
    date = datetime.datetime.today().strftime("%m.%d.%Y")
    data = [call.from_user.id, call.from_user.full_name, date]

    for key in state_data.keys():
        try:
            gsheet_dict[key] = state_data[key]
        except Exception:
            pass
    data.extend(list(gsheet_dict.values()))

    google_client_manager = call.bot.get('google_client_manager')
    google_client = await google_client_manager.authorize()
    # key = '1lv-kpvCo66N8ynKl1wdLdh8q6NXwtxhQvzgJwh6Cf_8'
    key = call.bot.get('gsheet_key')
    spreadsheet = await google_client.open_by_key(key)
    worksheet = await spreadsheet.worksheet('StatZBot')
    await worksheet.append_row(data)
