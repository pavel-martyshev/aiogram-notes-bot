from aiogram.fsm.state import StatesGroup, State


class NotesSG(StatesGroup):
    notes_menu = State()
    add_note = State()
    notes_list = State()
    note = State()
