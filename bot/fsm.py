from aiogram.fsm.state import StatesGroup, State


class Zarplata(StatesGroup):
    amount = State()
    where = State()
    comment = State()

class DeleteState(StatesGroup):
    record_id = State()


