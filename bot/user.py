
from aiogram import Router, F
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, delete, func
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext


from .inline import get_callback_btns
from .fsm import Zarplata, DeleteState
from .db.models import User

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
async def cmd_start(message: Message):
    await message.answer("Что хотите сделать?", reply_markup=MAIN_KB)


@router.callback_query(F.data == 'add')
async def cmd_add(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('укажите сумму что бы добавить', reply_markup=None)
    await state.set_state(Zarplata.amount)

@router.message(Zarplata.amount)
async def cmd_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await state.set_state(Zarplata.where)
    await message.answer('Где заработал')

@router.message(Zarplata.where)
async def cmd_where(message: Message, state: FSMContext):
    await state.update_data(where=message.text)
    await state.set_state(Zarplata.comment)
    await message.answer('краткая инфа')


@router.message(Zarplata.comment)
async def cmd_comment(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(comment=message.text)

    data = await state.get_data()

    obj = User(
        amount=data['amount'],
        where=data['where'],
        comment=data['comment']
    )
    session.add(obj)
    await session.commit()
    await message.answer('Запись добавлена в базу')
    await state.clear()



#Показывает бд
@router.callback_query(F.data == 'all_private')
async def show_all_records(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    result = await session.execute(select(User))
    records = result.scalars().all()

    if not records:
        await callback.message.answer("Записей пока нет.")
        return

    text = "📊 Все записи:\n\n"

    for rec in records:
        text += (
            f"💰 Сумма: {rec.amount}\n"
            f"📍 Где: {rec.where}\n"
            f"📝 Коммент: {rec.comment}\n"
            f"🆔 ID: {rec.id}\n"
            "──────────────\n"
        )

    await callback.message.answer(text, parse_mode="HTML")



# Удалить
@router.callback_query(F.data == 'delete')
async def delete_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ID записи для удаления:")
    await state.set_state(DeleteState.record_id)


@router.message(DeleteState.record_id)
async def delete_record(message: Message, state: FSMContext, session: AsyncSession):
    if not message.text.isdigit():
        await message.answer("ID должен быть числом.")
        return

    record_id = int(message.text)

    # Проверяем, существует ли запись
    result = await session.execute(select(User).where(User.id == record_id))
    record = result.scalar_one_or_none()

    if not record:
        await message.answer("Запись с таким ID не найдена.")
        await state.clear()
        return

    await session.execute(delete(User).where(User.id == record_id))
    await session.commit()

    try:
        await message.answer(f"Запись с ID {record_id} удалена 🗑")
    except TelegramNetworkError:
        print("Сообщение не отправилось, но запись удалена")

    await state.clear()


# Общая сумма
@router.callback_query(F.data == 'sum')
async def show_total_sum(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    result = await session.execute(
        select(func.sum(User.amount))
    )

    total: int | None = result.scalar()

    if total is None:
        await callback.message.answer("Записей пока нет.")
        return

    await callback.message.answer(f"💰 Общая сумма всех записей: {total}")
