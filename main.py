"""
Скрипт представляет собой телеграмм-бота,
который принимает в себя мои траты
и заносит их в таблицу (Excel или Google Sheets, пока не определился)
"""


import gspread
from datetime import datetime


sheet_url = 'https://docs.google.com/spreadsheets/d/\
1KwKwZxuqO6JLDmIR1reVRtkjSkTFFmzGGWag_VkJegI/edit#gid=0'  # Тестовая таблица
sheet_page = str(datetime.now().strftime('%B'))                                 # лист с которым будем работать

spent_sum_cell = 'B33'          # в эту ячейку записываем сумму потраченную за месяц
curr_month_cell = sheet_page         # в эту ячейку записываем текущий месяц


def purchase_cell():
    return 'A' + str(datetime.now().day)


def spent_cell():
    return 'B' + str(datetime.now().day)


def main():
    gc = gspread.service_account(filename='gs_credentials.json')
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.add_worksheet(title=sheet_page, rows=100, cols=20)
    worksheet.clear()


if __name__ == '__main__':
    main()
