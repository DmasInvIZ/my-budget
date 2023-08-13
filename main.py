"""
Скрипт представляет собой телеграмм-бота,
который принимает в себя мои траты
и заносит их в таблицу (Excel или Google Sheets, пока не определился)
"""


import gspread
from datetime import datetime


sheet_url = 'https://docs.google.com/spreadsheets/d/\
1B2OCvHxln1Z8vPXe0Rv0dQQh6cU7KvkPtn_bNsKIKSc/edit#gid=0'  # Тестовая таблица
sheet_page = str(datetime.now().strftime('%B'))      # получаем название месяца

spent_sum_cell = 'B33'          # в эту ячейку записываем сумму потраченную за месяц
income_cell = 'B36'             # ячейка для записи общего дохода за месяц
curr_month_cell = sheet_page         # в эту ячейку записываем текущий месяц

gc = gspread.service_account(filename='gs_credentials.json')
sh = gc.open_by_url(sheet_url)


def get_purchase_cell():
    """Получает номер ячейки для траты по текущей дате"""
    return 'A' + str(datetime.now().day)


def get_spent_cell():
    """Получает номер ячейки для суммы по текущей дате"""
    return 'B' + str(datetime.now().day)


def new_sheet_create():
    """Создает лист с названием текущего месяца,
        если лист существует, выбирает лист с названием текущего месяца
        (в случае перезапуска скрита)"""
    try:
        worksheet = sh.add_worksheet(title=sheet_page, rows=40, cols=2)
        worksheet.update('A33', 'Покупка')
        worksheet.update('B33', 'Сумма')
        worksheet.update('A34', 'Всего потрачено:')
        worksheet.update('B34', "=СУММ(B1:B31)")
        worksheet.update('A35', 'Всего заработано:')
        print('Лист создан')
        print(worksheet)
        return worksheet
    
    except gspread.exceptions.APIError:
        print("Лист не создан, такой лист уже существует")
        worksheet = sh.worksheet(sheet_page)  # если лист существует то выбираем его для работы
        print("Выбираем - " + sheet_page)
        return worksheet
    
    except:
        print("Другая ошибка")
        print(Exception)


def add_purchase(*args):
    """Добавляет запись в строку с тратой на момент добавления"""
    purchase_cell = get_purchase_cell()
    spent_cell = get_spent_cell()
    list_args = list(args)
    for i in list_args:
        if i.isdigit():
            current_spent_val = a.acell(spent_cell).value
            if current_spent_val is None:
                a.update(spent_cell, i)
            else:
                result = int(i) + int(current_spent_val)
                a.update(spent_cell, result)
        else:
            current_purchase_val = a.acell(purchase_cell).value
            if current_purchase_val is not None:
                a.update(purchase_cell, current_purchase_val + i + '\n')
            else: a.update(purchase_cell, i+ '\n')


def add_income(income_value: int):
    """Добавляет запись в ячейку доходов"""
    curr_income_value = worksheet.acell(income_cell).value
    if curr_income_value is None:
        worksheet.update(income_cell, income_value)
    else:
        result = int(curr_income_value) + int(income_value)
        worksheet.update(income_cell, result)

    

new_sheet_create()  # изменить переменную
