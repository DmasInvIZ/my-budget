"""
Скрипт представляет собой телеграмм-бота,
который принимает в себя мои траты
и заносит их в таблицу (Excel или Google Sheets, пока не определился)
"""

import logging
import gspread
from datetime import datetime
import telebot
from telebot import types

logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w")

token = "6476141297:AAEX-qm0JttdQrv_CcgeBSBFAF3ynqlTKHI"
bot = telebot.TeleBot(token)

sheet_url = 'https://docs.google.com/spreadsheets/d/\
1B2OCvHxln1Z8vPXe0Rv0dQQh6cU7KvkPtn_bNsKIKSc/edit#gid=0'  # Тестовая таблица
sheet_page = str(datetime.now().strftime('%B'))  # получаем название месяца

spent_sum_cell = 'B33'  # в эту ячейку записываем сумму потраченную за месяц
income_cell = 'B35'  # ячейка для записи общего дохода за месяц
curr_month_cell = sheet_page  # в эту ячейку записываем текущий месяц

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
        если лист существует, выбирает лист с названием текущего месяца"""
    try:
        logging.debug("Пробуем создать лист")
        worksheet = sh.add_worksheet(title=sheet_page, rows=40, cols=2)
        worksheet.update('A33', 'Покупка')
        worksheet.update('B33', 'Сумма')
        worksheet.update('A34', 'Всего потрачено:')
        worksheet.update('B34', '=СУММ(B1:B31)')
        worksheet.update('A35', 'Всего заработано:')
        logging.debug("Лист создан")
        print('Лист создан')
        print(worksheet)
        return worksheet

    except gspread.exceptions.APIError:
        logging.debug("Лист уже существует")
        print("Лист не создан, такой лист уже существует")
        worksheet = sh.worksheet(sheet_page)  # если лист существует, то выбираем его для работы
        logging.debug(f"Выбран лист - {sheet_page}")
        print("Выбираем - " + sheet_page)
        return worksheet

    except:
        logging.debug("Ошибка", Exception)
        print("Другая ошибка---------------------------------------------")
        print(Exception)
        print("Другая ошибка---------------------------------------------")


def add_purchase(string: str):
    """Добавляет запись в строку с тратой на момент добавления"""
    sheet = new_sheet_create()
    purchase_cell = get_purchase_cell()
    spent_cell = get_spent_cell()
    print(string)
    list_string = string.split()
    print(list_string)
    for i in list_string:
        if i.isdigit():
            current_spent_val = sheet.acell(spent_cell).value
            if current_spent_val is None:
                sheet.update(spent_cell, int(i))
            else:
                result = int(i) + int(current_spent_val)
                sheet.update(spent_cell, result)
        else:
            current_purchase_val = sheet.acell(purchase_cell).value
            if current_purchase_val is not None:
                sheet.update(purchase_cell, current_purchase_val + i + '\n')
            else:
                sheet.update(purchase_cell, i + '\n')


def add_income(income_value: int):
    """Добавляет запись в ячейку доходов"""
    sheet = new_sheet_create()
    curr_income_value = sheet.acell(income_cell).value
    if curr_income_value is None:
        sheet.update(income_cell, income_value)
    else:
        result = int(curr_income_value) + int(income_value)
        sheet.update(income_cell, result)


@bot.message_handler(commands=["help"])
def help_msg(message):
    send_help_message = "Вот список доступных команд:"
    bot.send_message(message.chat.id, send_help_message)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    income_btn = types.KeyboardButton("Записать доход")
    spending_btn = types.KeyboardButton("Записать траты")
    markup.row(income_btn, spending_btn)
    send_start_message = f"Привет {message.from_user.first_name}. Выбери одно из действий:"
    bot.send_message(message.chat.id, send_start_message, reply_markup=markup)


@bot.message_handler()
def doing(message):
    if message.text == "Записать доход":
        bot.register_next_step_handler(message, adding_income)
        bot.send_message(message.chat.id, "Записываю...")
    elif message.text == "Записать траты":
        bot.register_next_step_handler(message, adding_spending)
        bot.send_message(message.chat.id, "Слушаю...")
    else:
        bot.send_message(message.chat.id, "Ниче не понял щас...")


def adding_spending(message):
    print("записать траты")
    add_purchase(message.text)
    bot.send_message(message.chat.id, "Добавлено")
    print("Добавлено " + message.text)
    logging.debug("Добавлено " + message.text)


def adding_income(message):
    print("записать доход")
    if message.text.isdigit():
        add_income(message.text)
        bot.send_message(message.chat.id, f"Добавлено {message.text}")
        print("Доход - " + message.text)
        logging.debug("Доход - " + message.text)
    else:
        bot.send_message(message.chat.id, "Введи число")


# sheet = new_sheet_create()
print("Started..")
bot.infinity_polling()
