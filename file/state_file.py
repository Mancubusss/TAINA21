from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    question = State()

class Rasilka(StatesGroup):
    msg = State()