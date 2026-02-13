
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import types
from .inline import get_callback_btns

router = Router()

MAIN_KB = get_callback_btns (
    btns={
        'Добавить запись': 'add',
        'Все записи': 'all_private',
        'Удалить запись': 'delete',
        'Общая сумма': 'sum'
    }

)

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=MAIN_KB)