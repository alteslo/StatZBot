import typing

import gspread_asyncio
# import gspread_formatting
from gspread_asyncio import AsyncioGspreadClient
# from gspread_formatting import CellFormat, Borders, Border, TextFormat


async def create_spreadsheet(client: AsyncioGspreadClient, spreadsheet_name: str):

    spreadsheet = await client.create(spreadsheet_name)
    spreadsheet = await client.open_by_key(spreadsheet.id)
    return spreadsheet


async def add_worksheet(async_spreadsheet: gspread_asyncio.AsyncioGspreadSpreadsheet,
                        worksheet_name: str):
    worksheet = await async_spreadsheet.add_worksheet(worksheet_name, rows=1000, cols=100)
    worksheet = await async_spreadsheet.worksheet(worksheet_name)
    return worksheet


async def share_spreadsheet(async_spreadsheet: gspread_asyncio.AsyncioGspreadSpreadsheet,
                            email: str, role: str = 'writer', perm_type: str = 'user'):
    await async_spreadsheet.share(email, perm_type=perm_type, role=role)


async def fill_in_data(worksheet: gspread_asyncio.AsyncioGspreadWorksheet, data: typing.Tuple[typing.Tuple]):
    # await worksheet.clear()
    '''headers_cells = [
        Cell(
            1, column, value=text
        ) for column, text in enumerate(headers, start=1)
    ]
    await worksheet.update_cells(
        headers_cells
    )'''
    # await worksheet.insert_row(headers)

    await worksheet.append_row(data)

    '''cells_list = []

    for n_row, row in enumerate(data, start=2):
        for n_col, value in enumerate(row, start=1):
            cells_list.append(
                Cell(
                    n_row, n_col, value=value
                )
            )

    await worksheet.insert_row(
        cells_list
    )'''
    # format_header(worksheet.ws)


"""def format_header(worksheet: gspread.Worksheet):
    worksheet.freeze(1, 0)
    gspread_formatting.format_cell_range(
        worksheet, name='1:1',
        cell_format=CellFormat(
            borders=Borders(
                top=Border(style='SOLID_THICK'),
                bottom=Border(style='SOLID_THICK'),
                right=Border(style='SOLID'),
                left=Border(style='SOLID'),
            ),
            textFormat=TextFormat(bold=True),
            wrapStrategy='WRAP'
        )
    )"""
