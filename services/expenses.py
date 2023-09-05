from datetime import datetime, date
import re

import db.db
from services.categories import *
from services.exceptions import NotCorrectMessage
from lexicon.lexicon import LEXICON_RU


class Message(NamedTuple):
    amount: str
    category_text: str


class Expense(NamedTuple):
    amount: str
    category_name: str


def add_expense(message: str) -> Expense:
    """Тут мы получаем сырое сообщение, парсим его и возвращаем сумму и категорию трат"""
    parsed_msg = parse_raw_msg(message)
    category = Categories().get_category(parsed_msg.category_text)
    db.insert("expense", {
        "amount": parsed_msg.amount,
        "created": _get_now_datetime(),
        "category_codename": category.codename,
        "raw_text": message})
    return Expense(amount=parsed_msg.amount,
                   category_name=category.name)


def delete_expenses():
    expenses_list = db.get_today_expenses_list()
    if not expenses_list:
        return "Нечего удалять.\nСегодня еще не было трат."
    result = []
    for index, expense in enumerate(expenses_list):
        s = f"/del{index} {expense[1]} {expense[3]}"
        result.append(s)
    answer = '\n'.join(result)
    return answer

def delete_one_expense(index: str):
    if index.isdigit():
        index = int(index)
    else:
        return "Not correct format"
    expenses_list = db.get_today_expenses_list()
    expense = expenses_list[index]
    category_name, amount = expense[3], expense[1]
    print(category_name, amount)
    print(type(category_name), type(amount))

    result = db.delete(category_name, amount)
    answer = f'Удалена трата: {result[3]} {result[1]}'

    return answer
def all_categories():
    categories = Categories().get_all_categories()
    lst = list(map(lambda c: c.name, categories))
    answer_msg = '\n'.join(lst)
    return answer_msg

def get_today_expenses() -> str:
    return db.today_stat()


def get_month_expenses() -> str:
    first_day_month = date(datetime.now().year, datetime.now().month, 1).isoformat()
    return db.month_stat(first_day_month)


def parse_raw_msg(raw_msg: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_msg)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise NotCorrectMessage(LEXICON_RU["error_txt"])

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    #print(f"Распарсили сообщение: Сумма {amount} (тип {type(amount)}), \n Категория {category_text} (тип {type(category_text)})")
    return Message(amount=amount, category_text=category_text)

def _get_now_datetime() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
