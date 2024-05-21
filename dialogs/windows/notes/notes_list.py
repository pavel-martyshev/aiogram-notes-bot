from operator import itemgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

from config.config import Config, load_config
from dialogs.windows.notes.getters import notes_list_getter, note_getter
from dialogs.windows.notes.handlers import get_note_handler, back_handler, remove_handler, save_page_number
from states import NotesSG

config: Config = load_config()

notes_list_window = Window(
    Format('{notes}', when='notes'),
    Format('{note}', when='note'),
    ScrollingGroup(
        Select(
            text=Format(text='{item[0]}'),
            item_id_getter=itemgetter(1),
            id='note',
            items='notes_items',
            on_click=get_note_handler
        ),
        id='notes_list',
        width=config.tg_bot.pag_page_size,
        height=config.tg_bot.pag_height,
        hide_on_single_page=True,
        on_page_changed=save_page_number,
        when='notes_items'
    ),
    Button(
        Format('{delete_btn}'),
        id='remove',
        on_click=remove_handler,
        when='note'
    ),
    Button(
        Format('{back_btn}'),
        id='back',
        on_click=back_handler
    ),
    getter=(notes_list_getter, note_getter),
    state=NotesSG.notes_list
)
