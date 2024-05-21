from typing import Union, Dict, List, Any

from redis.asyncio.client import Redis

from config.config import Config, load_config

# Load configuration
config: Config = load_config()

# Initialize Redis client
redis = Redis(host=config.db.host, port=config.db.port, db=config.db.db_num, decode_responses=True)


class DBInterface:
    """
    A static class to interface with a Redis database asynchronously.
    """

    @staticmethod
    async def set_data(name: Union[str, memoryview, bytes],
                       value: Union[str, bytes, int, float, memoryview]) -> Any:
        """
        Set a value in Redis.

        Args:
            name: The name of the key.
            value: The value to be set.

        Returns:
            The result of the Redis set operation.
        """
        return await redis.set(name=name, value=value)

    @staticmethod
    async def get_data(name: Union[str, memoryview, bytes]) -> Any:
        """
        Get a value from Redis.

        Args:
            name: The name of the key.

        Returns:
            The value associated with the key.
        """
        return await redis.get(name=name)

    @staticmethod
    async def append(key: Union[str, memoryview, bytes],
                     value: Union[str, bytes, int, float, memoryview]) -> int:
        """
        Append a value to a key in Redis.

        Args:
            key: The name of the key.
            value: The value to be appended.

        Returns:
            The length of the string after the append operation.
        """
        return await redis.append(key=key, value=value)

    @staticmethod
    async def hset_data(name: str, mapping: Dict[str, Union[str, bytes, int, float, memoryview]]) -> int:
        """
        Set multiple fields in a hash in Redis.

        Args:
            name: The name of the hash.
            mapping: A dictionary of field-value pairs to be set in the hash.

        Returns:
            The number of fields that were added.
        """
        return await redis.hset(name=name, mapping=mapping)

    @staticmethod
    async def hget_all(name: str) -> Dict[str, Union[str, bytes, int, float, memoryview]]:
        """
        Get all the fields and values in a hash from Redis.

        Args:
            name: The name of the hash.

        Returns:
            A dictionary of field-value pairs stored in the hash.
        """
        return await redis.hgetall(name=name)

    @staticmethod
    async def hdel(name: str, keys: List[Union[str, memoryview, bytes]]) -> int:
        """
        Delete one or more hash fields in Redis.

        Args:
            name: The name of the hash.
            keys: A list of keys to be deleted from the hash.

        Returns:
            The number of fields that were removed.
        """
        return await redis.hdel(name, *keys)
