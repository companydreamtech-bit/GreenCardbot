from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    waiting_conf_number = State()
    waiting_rej_reason = State()
    waiting_broadcast_content = State()
