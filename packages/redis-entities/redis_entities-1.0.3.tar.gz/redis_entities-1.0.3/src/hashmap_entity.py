import time
from .base_entity import BaseRedisEntity, RedisEntityMetaclass
from .parameters import require_string, require_bytes, b2timestamp, timestamp2b


class RedisHashmapEntity(BaseRedisEntity):
    """
    This class represents a HashMap that is stored in Redis.
    The HashMap is identified by a Prefix that specifies the name of the HashMap.
    A HashMap entry is identified by the Prefix and a unique identifier.
    The RedisHashmapEntity stores and loads all HashMap keys as strings, and all HashMap values as bytes.
    """

    Contents = {}

    @classmethod
    def _encrypt_kwargs_dict(cls, kwargs_dict):
        return {
            require_string(key): cls.encrypt_data(key, value)
            for key, value in kwargs_dict.items()
        }

    @classmethod
    def _decrypt_kwargs_dict(cls, kwargs_dict):
        return {
            require_string(key): cls.decrypt_data(key, value)
            for key, value in kwargs_dict.items()
        }

    @classmethod
    def store(cls, identifier, **kwargs):
        for keyword_arg in cls.Contents:
            if keyword_arg not in kwargs:
                raise AttributeError(
                    f"Key={keyword_arg} not specified. Please specify it through an keyword argument."
                )
        kwargs = cls._encrypt_kwargs_dict(kwargs)
        identifier = cls.build_identifier(identifier)
        cls.RedisClient.hset(identifier, mapping=kwargs)
        cls.add_expiration(identifier)
        return cls(identifier, **kwargs)

    @classmethod
    def exists(cls, identifier):
        return cls.RedisClient.exists(cls.build_identifier(identifier)) == 1

    @classmethod
    def load(cls, identifier):
        identifier = cls.build_identifier(identifier)
        return cls(
            identifier,
            **cls._decrypt_kwargs_dict(cls.RedisClient.hgetall(identifier)),
        )

    @classmethod
    def length(cls, identifier):
        return cls.RedisClient.hlen(cls.build_identifier(identifier))

    @classmethod
    def delete(cls, identifier):
        return cls.RedisClient.delete(cls.build_identifier(identifier))

    def __init__(self, identifier, **kwargs):
        self.identifier = identifier
        self.items = kwargs
        self._enforce_valid_entity()

    def __getattr__(self, item):
        if item in self.items:
            return self.items.get(item)
        raise AttributeError("Item not Found")

    def __delattr__(self, item):
        if item in self.items:
            self.items.pop(item)

    def _enforce_valid_entity(self):
        for keyword in self.Contents:
            if not hasattr(self, keyword):
                raise AttributeError(f"Key={keyword} not contained in Entity")
