from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    """
    Dataclass representing Telegram bot configuration.

    Attributes:
        token (str): The token of the Telegram bot.
        allowed_users (str): The list of allowed user IDs separated by commas.
        pag_page_size (int): The page size for pagination.
        pag_height (int): The height of the pagination.
    """
    token: str
    allowed_users: str
    pag_page_size: int
    pag_height: int


@dataclass
class Database:
    """
    Dataclass representing database configuration.

    Attributes:
        host (str): The host address of the database.
        port (int): The port number of the database.
        db_num (int): The database number.
    """
    host: str
    port: int
    db_num: int


@dataclass
class Config:
    """
    Dataclass representing the overall configuration.

    Attributes:
        tg_bot (TgBot): Telegram bot configuration.
        db (Database): Database configuration.
        logs_level (str): The logging level.
    """
    tg_bot: TgBot
    db: Database
    logs_level: str


def load_config(path: str | None = None) -> Config:
    """
    Loads the configuration from environment variables.

    Args:
        path (str, optional): The path to the .env file. Defaults to None.

    Returns:
        Config: The loaded configuration object.
    """
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env('TOKEN'), allowed_users=env('ALLOWED_USERS'),
                     pag_page_size=int(env('PAGE_SIZE')), pag_height=int(env('HEIGHT'))),
        db=Database(host=env('DB_HOST'), port=int(env('DB_PORT')), db_num=int(env('DB_NUMBER'))),
        logs_level=env('LOGS_LEVEL')
    )
