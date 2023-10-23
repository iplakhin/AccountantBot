from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

router: Router = Router()

@router.message(CommandStart())
async def start_bot(msg: Message):
    await msg.answer(text="welcome text")

@router.message(Command(commands=["help"]))
async def help(msg: Message):
    await msg.answer(text="help_text")
    
@router.message()
async def any_func(msg: Message):
    await msg.answer(text="any text")