import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from fluentogram import TranslatorHub

from config.config import Config, load_config
from dialogs.dialogs import notes_dialog
from log_config import logger
from middlewares.i18n import TranslatorRunnerMiddleware
from states.states import NotesSG
from database import redis
from utils.i18n import create_translator_hub

ic.prefix = ''

# Load configuration
config: Config = load_config()

# Setup storage with Redis
storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(prefix='notebot', with_destiny=True))
bot = Bot(token=config.tg_bot.token)
dp = Dispatcher(storage=storage, bot=bot)

# List of allowed users
allowed_users = config.tg_bot.allowed_users


async def _on_startup() -> None:
    """
    Function to be executed on bot startup.
    Logs the start of the bot.
    """
    logger.warning('Bot started')
    ic('Bot started')


async def _on_shutdown() -> None:
    """
    Function to be executed on bot shutdown.
    Logs the stop of the bot.
    """
    logger.warning('Bot stopped')


@dp.message(Command(commands=['start']))
async def root_handler(message: Message, dialog_manager: DialogManager) -> None:
    """
    Handler for the /start command.

    If the user is allowed, starts the notes dialog.

    Args:
        message: The incoming message with the /start command.
        dialog_manager: The dialog manager to control the state.
    """
    user_id = str(message.from_user.id)
    logger.info(f'User {user_id} joined')
    if message.text == '/start' and user_id in allowed_users:
        await dialog_manager.start(state=NotesSG.notes_menu, mode=StartMode.RESET_STACK, data={'page_number': 0})


async def run() -> None:
    """
    Main function to run the bot.

    Sets up the translator hub, middlewares, registers startup and shutdown
    events, includes routers, and starts polling.
    """
    translator_hub: TranslatorHub = create_translator_hub()
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.startup.register(_on_startup)
    dp.shutdown.register(_on_shutdown)
    dp.include_routers(notes_dialog)
    setup_dialogs(dp)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == '__main__':
    asyncio.run(run())
