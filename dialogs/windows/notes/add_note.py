from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Format

from dialogs.windows.notes.getters import add_note_menu_getter
from dialogs.windows.notes.handlers import save_note_handler, cancel_handler
from states import NotesSG

add_note_window = Window(
    Format('{note_title}', when='note_name'),
    Format('{note}', when='note_body'),
    MessageInput(
        func=save_note_handler,
        content_types=ContentType.TEXT,
    ),
    Back(
        Format('{cancel_btn}'),
        on_click=cancel_handler,
        id='cancel'
    ),
    getter=add_note_menu_getter,
    state=NotesSG.add_note
)
