from aiogram_dialog import Dialog

from dialogs.windows import notes_menu, add_note_window, notes_list_window

notes_dialog = Dialog(
    notes_menu,
    add_note_window,
    notes_list_window,
)
