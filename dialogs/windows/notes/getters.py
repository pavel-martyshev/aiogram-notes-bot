from typing import Dict, TYPE_CHECKING, Union, List, Any

from aiogram.types import Chat
from aiogram_dialog import DialogManager
from environs import Env
from fluentogram import TranslatorRunner

from database import DBInterface

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

# Load environment variables
env = Env()
env.read_env()

# Load configuration parameters
PAGE_SIZE = int(env('PAGE_SIZE'))
HEIGHT = int(env('HEIGHT'))

# Adjust PAGE_SIZE if HEIGHT is greater than 1
if HEIGHT > 1:
    PAGE_SIZE *= HEIGHT


async def _message_creator(notes_data: Dict[str, Any], manager: DialogManager) -> str:
    """
    Create a message string from notes data for pagination.

    Args:
        notes_data: Dictionary containing notes data.
        manager: Dialog manager instance.

    Returns:
        A formatted string representing the notes.
    """
    message = ""
    notes = list(notes_data.keys())
    page_number = manager.start_data['page_number']
    start_index = page_number * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    if start_index == len(notes):
        manager.start_data['page_number'] -= 1
        start_index -= PAGE_SIZE
        end_index -= PAGE_SIZE

    for index, item in enumerate(notes[start_index:end_index], start=start_index + 1):
        message += f"{index}. {item}\n"

    return message.rstrip('\n')


async def _get_notes_items(notes_data: Dict[str, Any]) -> List[tuple[int, str]]:
    """
    Get a list of note items for display.

    Args:
        notes_data: Dictionary containing notes data.

    Returns:
        A list of tuples containing the index and note key.
    """
    notes_list = []
    keys = list(notes_data.keys())

    for i, key in enumerate(keys):
        notes_list.append((i + 1, key))

    return notes_list


async def menu_texts_getter(i18n: TranslatorRunner, **kwargs) -> Dict[str, str]:
    """
    Get localized menu texts.

    Args:
        i18n: Translator runner instance.

    Returns:
        A dictionary containing localized menu texts.
    """
    return {
        'menu_text': i18n.command.select(),
        'list_text': i18n.notes.list(),
        'add_text': i18n.add.note()
    }


async def notes_list_getter(event_chat: Chat, dialog_manager: DialogManager, i18n: TranslatorRunner,
                            **kwargs) -> Dict[str, Union[List[tuple[int, str]], str]]:
    """
    Get the list of notes for a user.

    Args:
        event_chat: The chat instance.
        dialog_manager: Dialog manager instance.
        i18n: Translator runner instance.

    Returns:
        A dictionary containing the notes message and items.
    """
    user_id = str(event_chat.id)
    data = await DBInterface.hget_all(user_id)
    msg = await _message_creator(data, dialog_manager)
    notes_items = await _get_notes_items(data)

    if msg:
        return {'notes': msg, 'notes_items': notes_items, 'back_btn': i18n.back()}
    return {'notes': i18n.no.notes(), 'back_btn': i18n.back()}


async def note_getter(dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs) -> Dict[str, Union[str, bool]]:
    """
    Get a specific note from the dialog manager.

    Args:
        dialog_manager: Dialog manager instance.
        i18n: Translator runner instance.

    Returns:
        A dictionary containing the note and related actions.
    """
    note = dialog_manager.dialog_data.get('note')

    if note:
        return {'note': note, 'notes': False, 'notes_items': False,
                'delete_btn': i18n.delete(), 'back_btn': i18n.back()}
    return {'note': note, 'delete_btn': i18n.delete(), 'back_btn': i18n.back()}


async def add_note_menu_getter(dialog_manager: DialogManager, i18n: TranslatorRunner,
                               **kwargs) -> Dict[str, Union[bool, str]]:
    """
    Get the menu for adding a new note.

    Args:
        dialog_manager: Dialog manager instance.
        i18n: Translator runner instance.

    Returns:
        A dictionary containing the state of the add note menu.
    """
    note_name = dialog_manager.dialog_data.get('note_name')

    if not note_name:
        dialog_manager.dialog_data['note_name'] = True
        return {'note_name': True, 'note_title': i18n.enter.title(),
                'cancel_btn': i18n.cancel(), 'back_btn': i18n.back()}
    else:
        dialog_manager.dialog_data['note'] = True
        return {'note_body': True, 'note': i18n.enter.note(), 'cancel_btn': i18n.cancel(), 'back_btn': i18n.back()}
