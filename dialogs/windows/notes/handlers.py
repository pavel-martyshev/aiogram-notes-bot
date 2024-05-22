from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner

from database import DBInterface
from log_config import logger
from states import NotesSG

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

# Aliases for database functions
add_note = DBInterface.hset_data
get_all = DBInterface.hget_all
remove = DBInterface.hdel


async def _pop_extra_data(manager: DialogManager) -> None:
    """
    Remove extra data from the dialog manager's dialog data.

    Args:
        manager: Dialog manager instance.
    """
    manager.dialog_data.pop('note_name', None)
    manager.dialog_data.pop('note', None)


async def save_note_handler(message: Message, widget: MessageInput, manager: DialogManager) -> None:
    """
    Handle the saving of a note.

    Args:
        message: The message instance containing the note.
        widget: The message input widget.
        manager: Dialog manager instance.
    """
    if manager.dialog_data.get('note_name') and not manager.dialog_data.get('note'):
        manager.dialog_data['note_name'] = message.text
    else:
        i18n: TranslatorRunner = manager.middleware_data.get('i18n')
        name = manager.dialog_data['note_name']
        note = message.text

        user_id = str(message.from_user.id)

        await add_note(name=user_id, mapping={name.capitalize(): note})

        logger.info(f'{user_id} saved the note')

        await _pop_extra_data(manager)
        await message.answer(i18n.success())
        await manager.switch_to(state=NotesSG.notes_menu)

    await message.delete()


async def get_note_handler(call: CallbackQuery, button: Button, manager: DialogManager, note_name: str) -> None:
    """
    Handle the retrieval of a note.

    Args:
        call: The callback query instance.
        button: The button instance.
        manager: Dialog manager instance.
        note_name: The name of the note to retrieve.
    """
    user_id = str(call.from_user.id)
    data = await get_all(user_id)
    note = data.get(note_name)
    manager.dialog_data['note'], manager.dialog_data['note_name'] = note, note_name


async def save_page_number(call: CallbackQuery, scroll: ManagedScroll, manager: ManagerImpl) -> None:
    """
    Save the current page number in the dialog manager.

    Args:
        call: The callback query instance.
        scroll: The managed scroll instance.
        manager: Manager implementation instance.
    """
    manager.start_data['page_number'] = await scroll.get_page()


async def remove_handler(call: CallbackQuery, button: Button, manager: DialogManager) -> None:
    """
    Handle the removal of a note.

    Args:
        call: The callback query instance.
        button: The button instance.
        manager: Dialog manager instance.
    """
    user_id = str(call.from_user.id)
    note_name = manager.dialog_data.get('note_name')
    await remove(user_id, [note_name])
    logger.info(f'{user_id} deleted the note')
    await _pop_extra_data(manager)


async def cancel_handler(call: CallbackQuery, button: Button, manager: DialogManager) -> None:
    """
    Handle the cancellation of the current operation.

    Args:
        call: The callback query instance.
        button: The button instance.
        manager: Dialog manager instance.
    """
    if manager.dialog_data.get('note_name'):
        manager.dialog_data.pop('note_name')
    if manager.dialog_data.get('note'):
        manager.dialog_data.pop('note')


async def back_handler(call: CallbackQuery, button: Button, manager: DialogManager) -> None:
    """
    Handle the back button action.

    Args:
        call: The callback query instance.
        button: The button instance.
        manager: Dialog manager instance.
    """
    note = manager.dialog_data.get('note')

    if note:
        await _pop_extra_data(manager)
    else:
        manager.start_data['start_amount'] = 0
        await manager.switch_to(NotesSG.notes_menu)
