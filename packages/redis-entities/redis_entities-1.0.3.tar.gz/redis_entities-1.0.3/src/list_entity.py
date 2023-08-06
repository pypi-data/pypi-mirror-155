from .base_entity import BaseRedisEntity


class RedisListEntity(BaseRedisEntity):
    @classmethod
    def lpush(cls, identifier, *values):
        identifier = cls.build_identifier(identifier)
        values = [cls.encrypt_data(identifier, value) for value in values]
        cls.RedisClient.lpush(identifier, *values)
        cls.add_expiration(identifier)

    @classmethod
    def brpop(cls, identifier, timeout=0):
        identifier = cls.build_identifier(identifier)
        key, value = cls.RedisClient.brpop(identifier, timeout=timeout)
        return key, cls.decrypt_data(identifier, value)

    @classmethod
    def lindex(cls, identifier, index):
        identifier = cls.build_identifier(identifier)
        value = cls.RedisClient.lindex(identifier, index)
        return cls.decrypt_data(identifier, value)

    @classmethod
    def length(cls, identifier):
        return cls.RedisClient.llen(cls.build_identifier(identifier))

    @classmethod
    def clear(cls, identifier):
        return cls.RedisClient.delete(cls.build_identifier(identifier))
