import re
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon import LEXICON_RU
from services import expenses

router: Router = Router()

def auth(func):
    async def wrapper(message: Message):
        if message.from_user.id != 544312899:
            return await message.answer("Access denied!")
        return await func(message)
    return wrapper

@router.message(CommandStart())
@auth
async def start_bot(msg: Message):
    await msg.answer(text=LEXICON_RU["welcome_txt"])

@router.message(Command(commands=["help"]))
async def help(msg: Message):
    await msg.answer(text=LEXICON_RU["help_txt"])

@router.message(Command(commands=["today"]))
@auth
async def today_stat(msg: Message):
    answer_msg = expenses.get_today_expenses()
    await msg.answer(text=LEXICON_RU["today_txt"] + answer_msg)


@router.message(Command(commands=["month"]))
@auth
async def month_stat(msg: Message):
    answer_msg = expenses.get_month_expenses()
    await msg.answer(text=LEXICON_RU["month_txt"] + answer_msg)

@router.message(Command(commands=["categories"]))
@auth
async def all_categories(msg: Message):
    answer_msg = expenses.all_categories()
    await msg.answer(text=LEXICON_RU["categories_txt"] + answer_msg)

@router.message(Command(commands=["delete"]))
@auth
async def delete_expenses(msg: Message):
    answer_msg = expenses.delete_expenses()
    await msg.answer(text=LEXICON_RU["delete_expense"] + answer_msg)


@router.message()
@auth
async def add_expense(msg: Message):
    reg = re.match(r"/del[\d]", msg.text)
    if reg:
        answer_msg = expenses.delete_one_expense(msg.text.replace('/del', ''))
        await msg.answer(text=answer_msg)
    else:
        expense = expenses.add_expense(msg.text)
        answer_message = f"Добавлены траты {expense.amount} € на {expense.category_name}"
        await msg.answer(text=answer_message)
