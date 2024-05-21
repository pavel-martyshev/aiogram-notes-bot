from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo
from aiogram_dialog.widgets.text import Format

from dialogs.windows.notes.getters import menu_texts_getter
from states import NotesSG

notes_menu = Window(
    Format('{menu_text}'),
    Group(
        SwitchTo(
            Format('{list_text}'),
            state=NotesSG.notes_list,
            id='notes_list',
        ),
        SwitchTo(
            Format('{add_text}'),
            state=NotesSG.add_note,
            id='add_note',
        ),
        width=2
    ),
    getter=menu_texts_getter,
    state=NotesSG.notes_menu
)
